import random
import time
from datetime import timedelta

import matplotlib.pyplot as plt
import networkx as nx
from faker import Faker

from zerok.graphiso import generator as graph_generator
from zerok.graphiso import isomorphism
from zerok.graphiso.credentials import hash_and_encode_data

SAMPLE_SIZE = 100_000

fake = Faker()

print(f"Testing {SAMPLE_SIZE} users...")

print("Generating credentials...")
start = time.perf_counter()
credentials = [
    hash_and_encode_data(fake.email()) + hash_and_encode_data(fake.password(length=16)) for _ in range(SAMPLE_SIZE)
]
end = time.perf_counter()
print(f"Generating credentials took {timedelta(seconds=end - start)}")

print("Generating graphs...")
start = time.perf_counter()
graphs = [graph_generator.generate_graph_degree(c) for c in credentials]
end = time.perf_counter()
print(f"Generating graphs took {timedelta(seconds=end - start)}")

print("Generating automorphism groups...")
start = time.perf_counter()
aut_grps = [isomorphism.get_automorphism_group(g) for g in graphs]
end = time.perf_counter()
print(f"Generating automorphism groups took {timedelta(seconds=end - start)}")
aut_grp_sizes = [len(a) for a in aut_grps]

print(
    "Automorphism group statistics: ",
    min(aut_grp_sizes),
    max(aut_grp_sizes),
    sum(aut_grp_sizes) / SAMPLE_SIZE,
)

g = random.choice(graphs)
nx.draw(g, with_labels=True, font_weight="bold")
plt.show()
