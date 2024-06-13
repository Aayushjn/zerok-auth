from ..problem import Problem
from flask import Flask, request
from .dbconnect import Connection


class ZKServer:
    problem: Problem

    def __init__(self, problem: Problem) -> None:
        self.app = Flask(__name__)
        self.problem = problem
        self.db = Connection("zkp_users")
        self.setup_routes()

    def setup_routes(self):

        @self.app.route("/register", methods=["POST"])
        def register():

            payload = request.get_json()
            response = self.problem.register_user(payload, self.db)
            return response

    def run(self, host="127.0.0.1", port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)
