import networkx as nx


def get_adjacency_list(g: nx.Graph) -> dict[int, list[int]]:
    return nx.to_dict_of_lists(g)


def get_mapping(g: nx.Graph, remapped_nodes: list[int]) -> dict[int, int]:
    nodes = list(g.nodes)
    return {nodes[i]: remapped_nodes[i] for i in range(len(nodes))}
