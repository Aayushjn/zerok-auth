import random
import time
from datetime import timedelta

import matplotlib.pyplot as plt
import networkx as nx
from faker import Faker

from zkg_client.crypto import hash_and_encode_data
from zkg_client.graph import generator as graph_generator
from zkg_client.graph import isomorphism

SAMPLE_SIZE = 200_000
DIRECTED = True

fake = Faker()

idx = random.randrange(SAMPLE_SIZE)
min_graph = [999999, 999999]
max_graph = [-1, -1]
graph_sum = [0, 0]
min_aut_grp = 999999
max_aut_grp = -1
aut_grp_sum = 0

start = time.perf_counter()
for i in range(1, SAMPLE_SIZE + 1):
    print(f"Testing {i}/{SAMPLE_SIZE}", end="\r")
    creds = hash_and_encode_data(fake.email()) + hash_and_encode_data(fake.password(length=16))
    graph = graph_generator.generate_graph_degree(creds, degree=32, directed=DIRECTED)
    aut_grp = isomorphism.get_automorphism_group(graph)

    node_len = len(graph.nodes)
    edge_len = len(graph.edges)
    if min_graph[0] > node_len:
        min_graph[0] = node_len
        min_graph[1] = edge_len
    if max_graph[0] < node_len:
       max_graph[0] = node_len
       max_graph[1] = edge_len
    graph_sum[0] += node_len
    graph_sum[1] += edge_len

    aut_grp_len = len(aut_grp)
    if min_aut_grp > aut_grp_len:
       min_aut_grp = aut_grp_len
    if max_aut_grp < aut_grp_len:
       max_aut_grp = aut_grp_len
    aut_grp_sum += aut_grp_len

    if i == idx:
        g = graph
end = time.perf_counter()

graph_avg = [graph_sum[0] // SAMPLE_SIZE, graph_sum[1] // SAMPLE_SIZE]
aut_grp_avg = aut_grp_sum // SAMPLE_SIZE

print(f"Took {timedelta(seconds=(end - start) / SAMPLE_SIZE)} on average")

print(f"Graphs: Min {min_graph[0]}, {min_graph[1]}", f"Max {max_graph[0]}, {max_graph[1]}", f"Avg {graph_avg[0]}, {graph_avg[1]}", sep="\t")
print(f"AutGrp: Min {min_aut_grp}", f"Max {max_aut_grp}", f"Avg {aut_grp_avg}", sep="\t")

nx.draw(g, with_labels=True, font_weight="bold")
plt.show()
