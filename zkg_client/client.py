import random
from copy import deepcopy
from typing import Any

import requests

from .crypto import hash_and_encode_data
from .graph import generator as graph_generator
from .graph import graph
from .graph import isomorphism

_server_config = {}


def configure_server(url: str):
    _server_config["url"] = url


def register_user(username: str, password: str) -> tuple[bool, dict[str, Any]]:
    if "url" not in _server_config:
        raise ValueError("Server not configured")

    encoded = hash_and_encode_data(username) + hash_and_encode_data(password)

    g1 = graph_generator.generate_graph_degree(encoded)
    adj_dict_g1 = graph.get_adjacency_list(g1)
    autgrp = isomorphism.get_automorphism_group(g1)
    g2_vertex_seq = autgrp[-1]

    pi = graph.get_mapping(g1, g2_vertex_seq)

    g2 = isomorphism.apply_isomorphic_mapping(g1, pi)
    adj_dict_g2 = graph.get_adjacency_list(g2)

    response = requests.post(
        url=f"{_server_config['url']}/register", json={"username": username, "G1": adj_dict_g1, "G2": adj_dict_g2}
    )

    return response.ok, response.json()


def login(username: str, password: str) -> tuple[bool, dict[str, Any]]:
    if "url" not in _server_config:
        raise ValueError("Server not configured")

    encoded = hash_and_encode_data(username) + hash_and_encode_data(password)
    g1 = graph_generator.generate_graph_degree(encoded)

    autgrp = isomorphism.get_automorphism_group(g1)
    g2_vertex_seq = autgrp[-1]
    pi = graph.get_mapping(g1, g2_vertex_seq)

    while True:
        a = random.randint(1, 2)
        iso = random.choice(autgrp)
        epsilon = graph.get_mapping(g1, iso)
        h = isomorphism.apply_isomorphic_mapping(g1, epsilon)
        print(f"{str(h)=}")
        print(f"{str(g1)=}")
        epsilon_inverse = isomorphism.get_isomorphic_mapping(h, g1)

        response = requests.post(
            url=f"{_server_config['url']}/login",
            json={"username": username, "h": graph.get_adjacency_list(h)},
        )
        if not response.ok:
            return False, response.json()

        b = response.json()["b"]

        if a == b:
            chi = epsilon_inverse
        elif a == 1 and b == 2:
            inter_graph = isomorphism.apply_isomorphic_mapping(
                isomorphism.apply_isomorphic_mapping(deepcopy(g1), pi),
                epsilon_inverse,
            )
            chi = isomorphism.get_isomorphic_mapping(g1, inter_graph)
        else:
            inter_graph = isomorphism.apply_isomorphic_mapping(
                isomorphism.apply_isomorphic_mapping(deepcopy(g1), epsilon_inverse),
                pi,
            )
            chi = isomorphism.get_isomorphic_mapping(g1, inter_graph)

        response = requests.post(
            url=f"{_server_config['url']}/verify",
            json={"username": username, "chi": chi},
        )
        if not response.ok:
            return False, response.json()

        status = response.json()["status"]
        if status == "success":
            return True, {}
        elif status == "failure":
            return False, response.json()


configure_server("http://127.0.0.1:5000")
login("admin", "admin")
