from flask import Flask
from flask import request
import networkx as nx
from ..problem import Problem
from ..util import format_dict_payload, compare_adj_lists
from .dbconnect import Connection
from .cache import update, get, delete
from ..graphiso import graph


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
                "parameters": [
                    format_dict_payload(param, False) for param in payload["parameters"]
                ],
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
                    "status": "failure",
                    "message": f"Username {payload['username']} not found",
                }, 404

            batch_no = payload["batch_no"]
            batch_params = [
                format_dict_payload(str_adj_dict)
                for str_adj_dict in payload["parameters"]
            ]
            batch_challenge = self.problem.generate_challenge(
                batch_size=self.app.config["BATCH_SIZE"]
            )
            update(payload["username"], batch_no, batch_params, batch_challenge)

            return {
                "status": "success",
                "challenges": batch_challenge,
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

            user_cache = get(payload["username"])
            batch_params = user_cache["batch_params"]
            batch_challenge = user_cache["batch_challenge"]
            batch_response = payload["responses"]

            for i in range(self.app.config["BATCH_SIZE"]):
                h = nx.from_dict_of_lists(batch_params[i])
                chi = format_dict_payload(batch_response[i])
                remapped_graph = graph.apply_isomorphic_mapping(h, chi)
                remap_adj_list = graph.get_adjacency_list(remapped_graph)

                if batch_challenge[i] == 1:
                    g1_adj_list = {int(k): v for k, v in user["parameters"][0].items()}
                    if compare_adj_lists(remap_adj_list, g1_adj_list):
                        continue
                    else:
                        delete(payload["username"])
                    return {"status": "failure", "message": "Login failed"}, 401
                else:
                    g2_adj_list = {int(k): v for k, v in user["parameters"][1].items()}
                    if compare_adj_lists(remap_adj_list, g2_adj_list):
                        continue
                    else:
                        delete(payload["username"])
                    return {"status": "failure", "message": "Login failed"}, 401
            
            delete(payload["username"])
            return {"status": "success"}, 200

    def run(self, host="127.0.0.1", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
