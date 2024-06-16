import requests

from .. import util
from ..problem import Problem


class ZKClient:
    problem: Problem
    server_url: str
    batch_size: int

    def __init__(self, problem: Problem, server_url: str):
        self.problem = problem
        self.server_url = server_url

        response = requests.get(f"{self.server_url}/negotiate")
        if response.ok:
            data = response.json()
            self.batch_size = data["batch_size"]
        else:
            self.batch_size = 1

    def user_registration(self, username: str, password: str):
        reg_params = self.problem.derive_registration_parameters(username, password)

        parameters = {
            "username": username,
            "parameters": [util.pre_format_dict(param) for param in reg_params],
        }

        response = requests.post(
            url=f"{self.server_url}/register",
            json=parameters,
        )

        return response.ok, response.json()

    def user_login(self, username: str, password: str):
        auth_params = self.problem.derive_auth_parameters(
            username, password, batch_size=self.batch_size
        )

        parameters = {
            "username": username,
            "parameters": [
                util.pre_format_dict(param["h"]) for param in auth_params["params"]
            ],
        }

        response = requests.post(f"{self.server_url}/login", json=parameters)
        if not response.ok:
            return False, response.json()

        challenges = response.json()["challenges"]
        challenge_responses = self.problem.generate_responses(
            challenges, auth_params["params"], auth_params["other_params"]
        )

        response = requests.post(
            f"{self.server_url}/verify",
            json={
                "username": username,
                "responses": [util.pre_format_dict(r) for r in challenge_responses],
            },
        )
        if not response.ok:
            return False, response.json()

        # TODO:A loop for sending the above received params batch wise to the server by calling /login endpoint
        # for receiving the challenges for that batch

        # TODO: receive challenges from the server for the sent login_params
        # TODO: send response to the server for the received challenges
