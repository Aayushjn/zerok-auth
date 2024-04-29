import matplotlib.pyplot as plt
import networkx as nx
from pynauty import graph


def generate_graph_repeat_conn(hash_data: bytes) -> nx.Graph:
    encoded_len = len(hash_data)
    mapping = {}

    mapping_idx = 0
    g = nx.MultiGraph()
    for i in range(encoded_len):
        prev_node = hash_data[i - 1]
        cur_node = hash_data[i]
        next_node = hash_data[(i + 1) % encoded_len]

        if cur_node not in mapping:
            mapping[cur_node] = mapping_idx
            mapping_idx += 1

        if g.has_node(cur_node):
            if not g.has_node(next_node):
                g.add_node(next_node)
                i += 1
                g.add_edge(prev_node, next_node)
        else:
            g.add_node(cur_node)

    return nx.relabel_nodes(g, mapping, copy=True)


def generate_graph_skip(hash_data: bytes) -> nx.Graph:
    encoded_len = len(hash_data)
    mapping = {}

    mapping_idx = 0
    g = nx.MultiGraph()
    for i in range(encoded_len):
        cur_node = hash_data[i]
        next_node = hash_data[(i + (2 ** (i % 8))) % encoded_len]

        if cur_node not in mapping:
            mapping[cur_node] = mapping_idx
            mapping_idx += 1

        if g.has_node(cur_node):
            if not g.has_node(next_node):
                g.add_node(next_node)
            g.add_edge(cur_node, next_node)
        else:
            g.add_node(cur_node)

    return nx.relabel_nodes(g, mapping, copy=True)


def generate_graph_degree(hash_data: bytes, degree: int = 8) -> nx.Graph:
    encoded_len = len(hash_data)
    mapping = {}

    mapping_idx = 0
    g = nx.Graph()
    temp_degree = degree
    for i in range(encoded_len):
        cur_node = hash_data[i]
        if not g.has_node(cur_node):
            g.add_node(cur_node)

        if cur_node not in mapping:
            mapping[cur_node] = mapping_idx
            mapping_idx += 1

        for j in range(temp_degree):
            next_node = hash_data[(i + (2**j)) % encoded_len]

            if not g.has_node(next_node):
                g.add_node(next_node)
                g.add_edge(cur_node, next_node)

        if temp_degree == 0:
            temp_degree = degree // 2
        else:
            degree -= 1

    h = nx.relabel_nodes(g, mapping, copy=True)
    return h
