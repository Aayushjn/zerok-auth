from flask import Flask
from flask import request

from . import cache
from ..problem import Problem
from ..util import format_dict_payload
from .dbconnect import Connection


class ZKServer:
    problem: Problem

    def __init__(self, problem: Problem):
        self.app = Flask(__name__)
        self.app.config.from_pyfile("config.py")
        self.problem = problem
        self.db = Connection("zkp_users")
        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/negotiate", methods=["GET"])
        def negotiate():
            return {
                "batch_size": self.app.config["BATCH_SIZE"],
                "rounds": self.app.config["ROUNDS"],
            }, 200

        @self.app.route("/register", methods=["POST"])
        def register():
            payload = request.get_json()

            collection = self.db["user_data"]

            if collection.find_one({"username": payload["username"]}) is not None:
                return {"message": "Username already registered"}, 400

            db_data = {
                "username": payload["username"],
                "parameters": [format_dict_payload(param, False) for param in payload["parameters"]],
            }

            result = collection.insert_one(db_data)
            if not result.inserted_id:
                return {"message": "Failed to register user"}, 500
            else:
                return {"message": "Registration Successful"}, 200

        @self.app.route("/login", methods=["POST"])
        def login():
            payload = request.get_json()

            collection = self.db["user_data"]

            # check if user is registered
            user = collection.find_one({"username": payload["username"]})

            if user is None:
                return {
                    "message": f"Username {payload['username']} not found",
                }, 404

            batch = payload["batch"]
            params = [format_dict_payload(str_adj_dict) for str_adj_dict in payload["parameters"]]
            challenges = self.problem.generate_challenges(batch_size=self.app.config["BATCH_SIZE"])
            cache.update(payload["username"], batch, params, challenges)

            return {
                "challenges": challenges,
            }, 200

        @self.app.route("/verify", methods=["POST"])
        def verify():
            payload = request.get_json()
            collection = self.db["user_data"]

            user = collection.find_one({"username": payload["username"]})

            if user is None:
                return {
                    "status": "failure",
                    "message": f"{payload['username']} not found",
                }, 404

            user_cache = cache.get(payload["username"])
            params = user_cache["params"]
            challenges = user_cache["challenges"]
            responses = payload["responses"]
            if len(responses) != len(challenges):
                return {
                    "status": "failure",
                    "message": "Illegal batch size",
                }, 400

            passed = self.problem.verify(params, responses, challenges, user["parameters"])
            cache.delete(payload["username"])
            if passed:
                return {"status": "success"}, 200
            else:
                return {"status": "failure", "message": "Login failed"}, 401

    def run(self, host="127.0.0.1", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
