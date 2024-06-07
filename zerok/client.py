from graphiso.graphiso import GraphIsomorphism
from problem import Problem

class ZKFramework:
    def __init__(self, hardproblem: Problem) -> None:
        self.hardproblem = hardproblem

    def register_user(self, username: str, password: str):

        (adj_G1, adj_G2) = self.hardproblem.derive_registration_parameters(username, password)

    






if __name__ == '__main__':

    # initialize the Zero Knowledge Framework

    hardproblem = GraphIsomorphism()
    zk_framework = ZKFramework(hardproblem)

    # user registration - accept username and password from user
    username = 'adwaitgondhalekar'
    password = 'kihjbuiergf883494'

    # derive parameters from credentials and store them
    zk_framework.register_user(username, password)

    # user authentication