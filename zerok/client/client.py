from .. import zkframework as zkf
import requests, json
from base64 import b64encode

class Client:
    def __init__(self) -> None:
        self.zk_framework = zkf.ZKFramework()
        self.server_url = "http://127.0.0.1:5000"

    def pre_format_dict(self, d: dict) -> str:
        return b64encode(json.dumps(d).encode()).decode()

    def user_registration(self, username: str, password: str):
        reg_params = self.zk_framework.register_user(username, password)

        # TODO:need to send the above received params and username to the server
        parameters = {"username": username,
                      "parameters": {},}

        for cnt, p in enumerate(reg_params):
            beta = "B"+str(cnt)
            # print(type(p))
            parameters["parameters"][beta] = self.pre_format_dict(p)
        
        response = requests.post(
        url=f"{self.server_url}/register",
        json=parameters,
        )

        return response.ok, response.json()


    def user_login(self, username: str, password: str):
        login_params = self.zk_framework.authenticate_user(username, password)

        # TODO: need to send the above received login_params to the server for saving to DB
        # TODO: receive challenges from the server for the sent login_params
        # TODO: send response to the server for the received challenges