from graphiso.graphiso import GraphIsomorphism


class ZKFramework:
    def __init__(self) -> None:
        self.hardproblem = GraphIsomorphism()

    def register_user(self, username: str, password: str):

        registration_params = self.hardproblem.derive_registration_parameters(username, password)

        return registration_params
    
    def authenticate_user(self, username: str, password: str):

        authentication_params = self.hardproblem.derive_auth_parameters(username, password)

        return authentication_params