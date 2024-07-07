import os

import argon2
from flask import Flask
from flask import request

from . import cache
from . import db
from ..problem import Problem
from ..util import format_dict_payload


class ZKServer:
    app: Flask
    problem: Problem
    client: db.DB
    ph: argon2.PasswordHasher

    def __init__(self, problem: Problem):
        self.app = Flask(__name__)
        self.app.config.from_prefixed_env("ZEROK")
        self.problem = problem
        self.db = db.DB(
            self.app.config["DB_HOST"],
            self.app.config["DB_PORT"],
            self.app.config["DB_USER"],
            self.app.config["DB_PASS"],
            self.app.config["DB_NAME"],
        )
        self.setup_routes()
        self.setup_traditional_routes()
        self.ph = argon2.PasswordHasher()

    def setup_traditional_routes(self):
        @self.app.route("/register_traditional", methods=["POST"])
        def register_traditional():
            payload = request.get_json()
            collection = self.db.get_collection("user_data_traditional")

            if collection.find_one({"username": payload["username"]}) is not None:
                return {"message": "Username already registered"}, 400

            salt = os.urandom(16)
            hashed_pw = self.ph.hash(password=payload["password"], salt=salt)

            db_data = {
                "username": payload["username"],
                "password": hashed_pw,
            }
            result = collection.insert_one(db_data)
            if not result.inserted_id:
                return {"message": "Failed to register user"}, 500
            else:
                return {"message": "Registration Successful"}, 200

        @self.app.route("/login_traditional", methods=["POST"])
        def login_traditional():
            payload = request.get_json()
            collection = self.db.get_collection("user_data_traditional")

            user = collection.find_one({"username": payload["username"]})

            if user is None:
                return {
                    "status": "failure",
                    "message": f"Username {payload['username']} not found",
                }, 404

            stored_pw = user["password"]
            try:
                result = self.ph.verify(hash=stored_pw, password=payload["password"])
                if result:
                    return {"status": "success"}, 200
            except (
                argon2.exceptions.VerificationError,
                argon2.exceptions.InvalidHashError,
            ) as e:
                return {"status": "failure", "message": str(e)}, 401

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
            collection = self.db.get_collection("user_data")

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
            collection = self.db.get_collection("user_data")

            # check if user is registered
            user = collection.find_one({"username": payload["username"]})

            if user is None:
                return {
                    "message": f"Username {payload['username']} not found",
                }, 404

            batch = payload["batch"]
            total_rounds = self.app.config["ROUNDS"]
            batch_size = self.app.config["BATCH_SIZE"]
            size = (
                batch_size
                if total_rounds % batch_size == 0 or batch < (total_rounds // batch_size) + 1
                else total_rounds - ((batch - 1) * batch_size)
            )
            params = [format_dict_payload(str_adj_dict) for str_adj_dict in payload["parameters"]]
            challenges = self.problem.generate_challenges(batch_size=size)
            cache.update(payload["username"], batch, params, challenges)

            return {
                "challenges": challenges,
            }, 200

        @self.app.route("/verify", methods=["POST"])
        def verify():
            payload = request.get_json()
            collection = self.db.get_collection("user_data")

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
            # expected = self.app.config["BATCH_SIZE"] if
            if len(responses) != len(challenges):
                print(len(responses), len(challenges))
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
        try:
            self.app.run(host=host, port=port, debug=debug)
        except:
            self.db.close()
