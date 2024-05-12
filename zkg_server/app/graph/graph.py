import networkx as nx


def build_graph(adj_list: dict[int, list[int]]) -> nx.Graph:
    return nx.Graph(adj_list)


def apply_isomorphic_mapping(g: nx.Graph, mapping: dict[int, int]):
    return nx.relabel_nodes(g, mapping, copy=True)


def get_adjacency_list(g: nx.Graph) -> dict[int, list[int]]:
    return nx.to_dict_of_lists(g)
