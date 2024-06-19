import networkx as nx


def get_adjacency_list(g: nx.Graph) -> dict[int, list[int]]:
    return nx.to_dict_of_lists(g)


def get_mapping(g: nx.Graph, remapped_nodes: list[int]) -> dict[int, int]:
    return dict(zip(g.nodes, remapped_nodes))


def apply_isomorphic_mapping(g: nx.Graph, mapping: dict[int, int]):
    return nx.relabel_nodes(g, mapping, copy=True)


def from_adjacency_list(adj_list: dict[int, list[int]]) -> nx.Graph:
    return nx.from_dict_of_lists(adj_list, create_using=nx.MultiGraph)
