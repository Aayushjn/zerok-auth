import random
from typing import Any
from typing import Iterable


from ..problem import Problem
from .credentials import hash_and_encode_data
from .generator import generate_graph_degree
from .graph import get_adjacency_list
from .graph import get_mapping
from .isomorphism import apply_isomorphic_mapping
from .isomorphism import get_automorphism_group
from .util import format_dict_payload


class GraphIsomorphism(Problem):

    def derive_registration_parameters(
        self, username: str, password: str, **kwargs
    ) -> Iterable[Any]:
        encoded = hash_and_encode_data(username) + hash_and_encode_data(password)
        g1 = generate_graph_degree(encoded)
        adj_dict_g1 = get_adjacency_list(g1)
        autgrp = get_automorphism_group(g1)
        g2_vertex_seq = autgrp[-1]

        pi = get_mapping(g1, g2_vertex_seq)
        g2 = apply_isomorphic_mapping(g1, pi)
        adj_dict_g2 = get_adjacency_list(g2)

        return adj_dict_g1, adj_dict_g2

    def register_user(self, user_data, db) -> Iterable[Any]:

        
        collection = db["user_data"]

        if collection.find_one({"username": user_data["username"]}) is not None:
            return {"message": "Username already registered"}, 400

        # db_data = {
        #     "username": user_data["username"],
        #     "G1": format_dict_user_data(user_data["G1"], False),
        #     "G2": format_dict_user_data(user_data["G2"], False),
        # }

        db_data = {
            "username": user_data["username"],
            "parameters": {},
        }

        for k, v in user_data["parameters"].items():
            db_data["parameters"][k] = format_dict_payload(v, False)

        result = collection.insert_one(db_data)
        if not result.inserted_id:
            return {"message": "Failed to register user"}, 500
        else:
            return {"message": "Registration Successful"}, 200

    def derive_auth_parameters(
        self, username: str, password: str, **kwargs
    ) -> Iterable[Any]:
        rounds = kwargs.pop("rounds", 1)

        encoded = hash_and_encode_data(username) + hash_and_encode_data(password)
        g1 = generate_graph_degree(encoded, rounds)
        autgrp = get_automorphism_group(g1)
        g2_vertex_seq = autgrp[-1]

        pi = get_mapping(g1, g2_vertex_seq)
        g2 = apply_isomorphic_mapping(g1, pi)

        params = []
        for _ in range(rounds):
            a = random.randint(1, 2)
            iso = random.choice(autgrp)
            src_graph = g1 if a == 1 else g2
            epsilon = get_mapping(src_graph, iso)
            h = apply_isomorphic_mapping(src_graph, epsilon)

            params.append(
                {
                    "a": a,
                    "iso": iso,
                    "epsilon": epsilon,
                    "epsilon_inverse": {v: k for k, v in epsilon.items()},
                    "h": get_adjacency_list(h),
                }
            )

        return params

    def generate_response(self, challenge: Iterable[Any]) -> Iterable[Any]:
        pass

    def generate_challenge(self) -> Iterable[Any]:
        pass
