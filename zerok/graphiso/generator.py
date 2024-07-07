import networkx as nx


def generate_graph_repeat_conn(encoded_data: bytes) -> nx.Graph:
    encoded_len = len(encoded_data)
    mapping = {}

    mapping_idx = 0
    g = nx.MultiGraph()
    for i in range(encoded_len):
        prev_node = encoded_data[i - 1]
        cur_node = encoded_data[i]
        next_node = encoded_data[(i + 1) % encoded_len]

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


def generate_graph_skip(encoded_data: bytes) -> nx.Graph:
    encoded_len = len(encoded_data)
    mapping = {}

    mapping_idx = 0
    g = nx.MultiGraph()
    for i in range(encoded_len):
        cur_node = encoded_data[i]
        next_node = encoded_data[(i + (2 ** (i % 8))) % encoded_len]

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


def generate_graph_degree(encoded_data: bytes, degree: int = 16) -> nx.Graph:
    encoded_len = len(encoded_data)
    mapping = {}

    mapping_idx = 0
    g = nx.MultiGraph()
    temp_degree = degree
    for i in range(encoded_len):
        cur_node = encoded_data[i]
        if not g.has_node(cur_node):
            g.add_node(cur_node)

        if cur_node not in mapping:
            mapping[cur_node] = mapping_idx
            mapping_idx += 1

        for j in range(temp_degree):
            next_node = encoded_data[(i + (2**j)) % encoded_len]

            if not g.has_node(next_node):
                g.add_node(next_node)
                g.add_edge(cur_node, next_node)

        if temp_degree == 0:
            temp_degree = degree // 2
        else:
            temp_degree -= 1

    return nx.relabel_nodes(g, mapping, copy=True)