import random
import networkx as nx
from copy import deepcopy
from typing import Any
from typing import Iterable
from typing import Mapping

from ..problem import Problem
from .credentials import hash_and_encode_data
from .generator import generate_graph_degree
from .graph import get_adjacency_list
from .graph import get_mapping
from .isomorphism import apply_isomorphic_mapping
from .isomorphism import get_automorphism_group
from .isomorphism import get_isomorphic_mapping
from ..util import format_dict_payload


class GraphIsomorphism(Problem):
    batch_params: dict

    def __init__(self):
        super().__init__()
        self.batch_params = {}

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

    def derive_auth_parameters(
        self, username: str, password: str, **kwargs
    ) -> Mapping[str, Any]:
        total_rounds = kwargs["total_rounds"]
        encoded = hash_and_encode_data(username) + hash_and_encode_data(password)
        g1 = generate_graph_degree(encoded)
        autgrp = get_automorphism_group(g1)
        g2_vertex_seq = autgrp[-1]

        pi = get_mapping(g1, g2_vertex_seq)
        g2 = apply_isomorphic_mapping(g1, pi)
        pi_inverse = get_mapping(g2, list(g1.nodes))

        params = []
        for _ in range(total_rounds):
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

        return {"params": params, "other_params": {"pi": pi, "pi_inverse": pi_inverse}}

    def generate_responses(
        self,
        challenge: Iterable[Any],
        auth_params: Iterable[Any],
        other_params: Iterable[Any],
    ) -> Iterable[Any]:
        responses = []
        for c, param in zip(challenge, auth_params):
            if c == param["a"]:
                chi = param["epsilon_inverse"]
            elif param["a"] == 1 and c == 2:
                inter_graph = apply_isomorphic_mapping(
                    apply_isomorphic_mapping(
                        deepcopy(nx.from_dict_of_lists(param["h"])), param["epsilon_inverse"]
                    ),
                    other_params["pi"],
                )
                chi = get_isomorphic_mapping(nx.from_dict_of_lists(param["h"]), inter_graph)
            else:
                inter_graph = apply_isomorphic_mapping(
                    apply_isomorphic_mapping(
                        deepcopy(nx.from_dict_of_lists(param["h"])), param["epsilon_inverse"]
                    ),
                    other_params["pi_inverse"],
                )
                chi = get_isomorphic_mapping(nx.from_dict_of_lists(param["h"]), inter_graph)

            responses.append(chi)

        return responses

    def generate_challenge(self, **kwargs) -> Iterable[Any]:
        
        batch_size = kwargs.pop("batch_size", 1)
        batch_challenge = [random.randint(1, 2) for i in range(batch_size)]
        
        return batch_challenge
