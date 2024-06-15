import requests

from .. import util
from ..problem import Problem


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
                f"B{i}": util.pre_format_dict(param)
                for i, param in enumerate(reg_params)
            },
        }

        response = requests.post(
            url=f"{self.server_url}/register",
            json=parameters,
        )

        return response.ok, response.json()

    def user_login(self, username: str, password: str):

        profile_exists = requests.post(
            url=f"{self.server_url}/register",
            json = {
                "username": username
            },
        )

        if not profile_exists.ok:
            return profile_exists.ok, profile_exists.json()
        else:

            login_params = self.problem.derive_auth_parameters(username, password)

            # TODO:A loop for sending the above received params batch wise to the server by calling /login endpoint
            # for receiving the challenges for that batch


            # TODO: receive challenges from the server for the sent login_params
            # TODO: send response to the server for the received challenges
