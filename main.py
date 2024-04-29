from base64 import b85encode
from hashlib import sha3_512

import networkx as nx
from faker import Faker
from faker.providers import internet
import matplotlib.pyplot as plt
from pynauty import graph

from graphgen import generate_graph_degree

fake = Faker()
fake.add_provider(internet)

username = fake.email()
password = fake.password(16)

print(f"{username=}, {password=}")

hashed_un = sha3_512(username.encode()).digest()
hashed_pw = sha3_512(password.encode()).digest()
encoded_un = b85encode(hashed_un)
encoded_pw = b85encode(hashed_pw)
encoded = encoded_un + encoded_pw

# g = generate_graph_repeat_conn(encoded)
# g = generate_graph_skip(encoded)
g = generate_graph_degree(encoded, degree=16)
print(f"Constructed graph with {len(g.nodes)} vertices and {len(g.edges)} edges")

adj_dict = nx.to_dict_of_lists(g)
print(adj_dict)
png = graph.Graph(len(adj_dict), adjacency_dict=adj_dict)
generators, _, _, _, _ = graph.autgrp(png)
print(f"Found {len(generators)} isomorphisms\n{generators}")

nx.draw(g, with_labels=True, font_weight="bold")
plt.show()
