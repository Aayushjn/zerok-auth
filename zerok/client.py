from graphiso.graphiso import GraphIsomorphism
from zkframework import ZKFramework

class Client:
    def __init__(self) -> None:
        self.zk_framework = ZKFramework()

    def user_registration(self, username: str, password: str):
        params = self.zk_framework.register_user(username, password)

        # TODO:need to send the above received params and username to the server

    def user_login(self, username: str, password: str):
        login_params = self.zk_framework.authenticate_user(username, password)

        # TODO: need to send the above received login_params to the server for saving to DB
        # TODO: receive challenges from the server for the sent login_params
        # TODO: send response to the server for the received challenges