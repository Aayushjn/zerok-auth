from flask import Flask
from flask import request

from ..problem import Problem
from ..util import format_dict_payload
from .dbconnect import Connection


class ZKServer:
    problem: Problem

    def __init__(self, problem: Problem):
        self.app = Flask(__name__)
        self.problem = problem
        self.db = Connection("zkp_users")
        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/register", methods=["POST"])
        def register():
            payload = request.get_json()

            collection = self.db["user_data"]

            if collection.find_one({"username": payload["username"]}) is not None:
                return {"message": "Username already registered"}, 400

            db_data = {
                "username": payload["username"],
                "parameters": {},
            }

            for k, v in payload["parameters"].items():
                db_data["parameters"][k] = format_dict_payload(v, False)

            result = collection.insert_one(db_data)
            if not result.inserted_id:
                return {"message": "Failed to register user"}, 500
            else:
                return {"message": "Registration Successful"}, 200

    def run(self, host="127.0.0.1", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
