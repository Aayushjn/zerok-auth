import json
from base64 import b64encode

import requests

from ..problem import Problem


def pre_format_dict(d: dict) -> str:
    return b64encode(json.dumps(d).encode()).decode()


class ZKClient:
    problem: Problem

    def __init__(self, problem: Problem, server_url: str) -> None:
        self.problem = problem
        self.server_url = server_url

    def user_registration(self, username: str, password: str):
        reg_params = self.problem.derive_registration_parameters(username, password)

        # TODO:need to send the above received params and username to the server
        parameters = {
            "username": username,
            "parameters": {
                f"B{i}": pre_format_dict(param) for i, param in enumerate(reg_params)
            },
        }

        response = requests.post(
            url=f"{self.server_url}/register",
            json=parameters,
        )

        return response.ok, response.json()

    def user_login(self, username: str, password: str):
        login_params = self.problem.derive_auth_parameters(username, password)

        # TODO: need to send the above received login_params to the server for saving to DB
        # TODO: receive challenges from the server for the sent login_params
        # TODO: send response to the server for the received challenges
