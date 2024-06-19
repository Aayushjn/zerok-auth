import random
from typing import Any
from typing import Iterable
from typing import Mapping

from . import graph
from . import isomorphism
from .. import util
from ..problem import Problem
from .credentials import hash_and_encode_data
from .generator import generate_graph_degree


class GraphIsomorphism(Problem):
    def derive_registration_parameters(self, username: str, password: str, **kwargs) -> Iterable[Any]:
        encoded = hash_and_encode_data(username) + hash_and_encode_data(password)
        g1 = generate_graph_degree(encoded)
        adj_dict_g1 = graph.get_adjacency_list(g1)
        autgrp = isomorphism.get_automorphism_group(g1)
        g2_vertex_seq = autgrp[-1]

        pi = graph.get_mapping(g1, g2_vertex_seq)
        g2 = isomorphism.apply_isomorphic_mapping(g1, pi)
        adj_dict_g2 = graph.get_adjacency_list(g2)

        return adj_dict_g1, adj_dict_g2

    def derive_auth_parameters(self, username: str, password: str, **kwargs) -> Mapping[str, Any]:
        total_rounds = kwargs["total_rounds"]
        encoded = hash_and_encode_data(username) + hash_and_encode_data(password)
        g1 = generate_graph_degree(encoded)
        autgrp = isomorphism.get_automorphism_group(g1)
        g2_vertex_seq = autgrp[-1]

        pi = graph.get_mapping(g1, g2_vertex_seq)
        g2 = isomorphism.apply_isomorphic_mapping(g1, pi)
        pi_inverse = graph.get_mapping(g2, list(g1.nodes))

        params = []
        for _ in range(total_rounds):
            a = random.randint(1, 2)
            iso = random.choice(autgrp)
            src_graph = g1 if a == 1 else g2
            epsilon = graph.get_mapping(src_graph, iso)
            h = isomorphism.apply_isomorphic_mapping(src_graph, epsilon)

            params.append(
                {
                    "a": a,
                    "iso": iso,
                    "epsilon": epsilon,
                    "epsilon_inverse": {v: k for k, v in epsilon.items()},
                    "h": graph.get_adjacency_list(h),
                }
            )

        return {"params": params, "other_params": {"pi": pi, "pi_inverse": pi_inverse}}

    def generate_responses(
        self,
        challenge: Iterable[Any],
        auth_params: Iterable[Any],
        other_params: Mapping[str, Any],
    ) -> Iterable[dict[int, int]]:
        responses = []
        for c, param in zip(challenge, auth_params):
            if c == param["a"]:
                chi = param["epsilon_inverse"]
            elif param["a"] == 1 and c == 2:
                inter_graph = isomorphism.apply_isomorphic_mapping(
                    isomorphism.apply_isomorphic_mapping(
                        graph.from_adjacency_list(param["h"]),
                        param["epsilon_inverse"],
                    ),
                    other_params["pi"],
                )
                chi = isomorphism.get_isomorphic_mapping(graph.from_adjacency_list(param["h"]), inter_graph)
            else:
                inter_graph = isomorphism.apply_isomorphic_mapping(
                    isomorphism.apply_isomorphic_mapping(
                        graph.from_adjacency_list(param["h"]),
                        param["epsilon_inverse"],
                    ),
                    other_params["pi_inverse"],
                )
                chi = isomorphism.get_isomorphic_mapping(graph.from_adjacency_list(param["h"]), inter_graph)

            responses.append(chi)

        return responses

    def generate_challenges(self, **kwargs) -> Iterable[int]:
        batch_size = kwargs.pop("batch_size", 1)
        return [random.randint(1, 2) for _ in range(batch_size)]

    def verify(
        self, params: Iterable[Any], responses: Iterable[Any], challenges: Iterable[int], user_params: Iterable[Any]
    ) -> bool:
        for param, r, c in zip(params, responses, challenges):
            h = graph.from_adjacency_list(param)
            chi = util.format_dict_payload(r)
            remapped_graph = isomorphism.apply_isomorphic_mapping(h, chi)
            remap_adj_list = graph.get_adjacency_list(remapped_graph)

            if c == 1:
                g1_adj_list = {int(k): v for k, v in user_params[0].items()}
                if not util.compare_adj_lists(remap_adj_list, g1_adj_list):
                    return False
            else:
                g2_adj_list = {int(k): v for k, v in user_params[1].items()}
                if not util.compare_adj_lists(remap_adj_list, g2_adj_list):
                    return False

        return True
