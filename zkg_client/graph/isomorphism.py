import networkx as nx
from pynauty import graph


def get_automorphism_group(g: nx.Graph) -> list[list[int]]:
    adj_dict = nx.to_dict_of_lists(g)
    pn_graph = graph.Graph(len(adj_dict), adjacency_dict=adj_dict)

    return graph.autgrp(pn_graph)[0]


def apply_isomorphic_mapping(g: nx.Graph, mapping: dict[int, int]) -> nx.Graph:
    return nx.relabel_nodes(g, mapping, copy=True)


def get_isomorphic_mapping(g1: nx.Graph, g2: nx.Graph) -> dict[int, int]:
    return nx.vf2pp_isomorphism(g1, g2)


def is_isomorphic(g1: nx.Graph, g2: nx.Graph) -> bool:
    return nx.vf2pp_is_isomorphic(g1, g2)
