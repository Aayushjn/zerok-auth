from typing import Any

import requests

from .. import util
from ..problem import Problem


class ZKClient:
    problem: Problem
    server_url: str
    batch_size: int
    total_rounds: int

    def __init__(self, problem: Problem, server_url: str):
        self.problem = problem
        self.server_url = server_url

        response = requests.get(f"{self.server_url}/negotiate")
        if response.ok:
            data = response.json()
            self.batch_size = data["batch_size"]
            self.total_rounds = data["rounds"]
        else:
            self.batch_size = 1
            self.total_rounds = 10

    def register_user(self, username: str, password: str) -> tuple[bool, dict[str, Any]]:
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

    def login_user(self, username: str, password: str):
        auth_params = self.problem.derive_auth_parameters(username, password, total_rounds=self.total_rounds)

        for i in range(0, self.total_rounds, self.batch_size):
            batch = (i // self.batch_size) + 1
            parameters = {
                "username": username,
                "parameters": [
                    util.pre_format_dict(param["h"]) for param in auth_params["params"][i : (i + self.batch_size)]
                ],
                "batch": batch,
            }

            response = requests.post(f"{self.server_url}/login", json=parameters)
            if not response.ok:
                return False, response.json()

            challenges = response.json()["challenges"]

            challenge_responses = self.problem.generate_responses(
                challenges,
                auth_params["params"][i : (i + self.batch_size)],
                auth_params["other_params"],
            )

            response = requests.post(
                f"{self.server_url}/verify",
                json={
                    "username": username,
                    "responses": [util.pre_format_dict(r) for r in challenge_responses],
                },
            )

            if not response.ok:
                return response.ok, response.json()
            else:
                print(f"Batch {batch} completed successfully")

        return 200, {"message": "Login Successful"}
