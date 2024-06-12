from .graphiso.graphiso import GraphIsomorphism
from .problem import Problem


class ZKFramework:
    hard_problem: Problem

    def __init__(self) -> None:
        self.hard_problem = GraphIsomorphism()

    def register_user(self, username: str, password: str):

        registration_params = self.hard_problem.derive_registration_parameters(
            username, password
        )

        return registration_params

    def authenticate_user(self, username: str, password: str):

        authentication_params = self.hard_problem.derive_auth_parameters(
            username, password
        )

        return authentication_params
