import networkx as nx


def get_adjacency_list(g: nx.Graph) -> dict[int, list[int]]:
    return nx.to_dict_of_lists(g)


def get_mapping(g: nx.Graph, remapped_nodes: list[int]) -> dict[int, int]:
    return dict(zip(g.nodes, remapped_nodes))
