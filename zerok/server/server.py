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
        self.current_user = None
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
        
        @self.app.route("/if_profile_exists", methods=["POST"])
        def if_profile_exists():
            # payload is a JSON object with a signle member : username
            payload = request.get_json()

            collection = self.db["user_data"]

            # check if user is regsistered
            user = collection.find_one({"username": payload["username"]})

            if user is None:
                return {
                    "status": "failure",
                    "message": f"Username {payload['username']} not found",
                }, 404
            else:
                self.current_user = payload["username"]
                return {"status": "success"}, 200
        
        @self.app.route("/login", methods=["POST"])
        def login():
            # payload is a JSON object with a single member : batch_parameters 
            # batch_parameters is a a dict of dicts where key = round_number and value = adj dict of graph h
            payload = request.get_json()
            
            batch_challenge = self.problem.generate_challenge(payload["batch_parameters"])
            
    def run(self, host="127.0.0.1", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
