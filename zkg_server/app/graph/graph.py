import networkx as nx


def build_graph(adj_list: dict[int, list[int]]) -> nx.Graph:
    return nx.Graph(adj_list)


def apply_isomorphic_mapping(g: nx.Graph, mapping: dict[int, int]):
    return nx.relabel_nodes(g, mapping, copy=True)
