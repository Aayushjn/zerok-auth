import json
import random
from base64 import b64encode
from copy import deepcopy
from typing import Any

import requests

from .crypto import hash_and_encode_data
from .graph import generator as graph_generator
from .graph import graph
from .graph import isomorphism

_server_config = {}


def pre_format_dict(d: dict) -> str:
    return b64encode(json.dumps(d).encode()).decode()


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
        url=f"{_server_config['url']}/register",
        json={
            "username": username,
            "G1": pre_format_dict(adj_dict_g1),
            "G2": pre_format_dict(adj_dict_g2),
        },
    )

    return response.ok, response.json()


def register_user_traditional(
    username: str, password: str
) -> tuple[bool, dict[str, Any]]:
    if "url" not in _server_config:
        raise ValueError("Server not configured")
    response = requests.post(
        url=f"{_server_config['url']}/register_traditional",
        json={"username": username, "password": password},
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
    g2 = isomorphism.apply_isomorphic_mapping(g1, pi)
    pi_inverse = graph.get_mapping(g2, list(g1.nodes))

    round_num = 1
    while True:
        # print(f"Initiating round {round_num}")

        a = random.randint(1, 2)
        iso = random.choice(autgrp)
        if a == 1:
            epsilon = graph.get_mapping(g1, iso)
            h = isomorphism.apply_isomorphic_mapping(g1, epsilon)

            epsilon_inverse = {v: k for k, v in epsilon.items()}

        else:
            epsilon = graph.get_mapping(g2, iso)
            h = isomorphism.apply_isomorphic_mapping(g2, epsilon)
            epsilon_inverse = {v: k for k, v in epsilon.items()}

        response = requests.post(
            url=f"{_server_config['url']}/login",
            json={
                "username": username,
                "h": pre_format_dict(graph.get_adjacency_list(h)),
            },
        )
        if not response.ok:
            return False, response.json()

        b = response.json()["b"]

        if a == b:
            chi = epsilon_inverse
        elif a == 1 and b == 2:
            inter_graph = isomorphism.apply_isomorphic_mapping(
                isomorphism.apply_isomorphic_mapping(deepcopy(h), epsilon_inverse),
                pi,
            )
            chi = isomorphism.get_isomorphic_mapping(h, inter_graph)
        else:
            inter_graph = isomorphism.apply_isomorphic_mapping(
                isomorphism.apply_isomorphic_mapping(deepcopy(h), epsilon_inverse),
                pi_inverse,
            )
            chi = isomorphism.get_isomorphic_mapping(h, inter_graph)

        response = requests.post(
            url=f"{_server_config['url']}/verify",
            json={"username": username, "chi": pre_format_dict(chi)},
        )
        if not response.ok:
            return False, response.json()

        status = response.json()["status"]
        if status == "success":
            return True, {"message": "Login Successful"}
        elif status == "failure":
            return False, response.json()
        round_num += 1


def login_traditional(username: str, password: str) -> tuple[bool, dict[str, Any]]:
    if "url" not in _server_config:
        raise ValueError("Server not configured")

    response = requests.post(
        url=f"{_server_config['url']}/login_traditional",
        json={
            "username": username,
            "password": password,
        },
    )
    if not response.ok:
        return False, response.json()

    status = response.json()["status"]
    if status == "success":
        return True, {"message": "Login Successful"}
    elif status == "failure":
        return False, response.json()
