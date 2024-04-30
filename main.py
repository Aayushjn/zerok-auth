from base64 import b85encode, b64encode, b64decode
from hashlib import sha3_512

import networkx as nx
from faker import Faker
from faker.providers import internet
import matplotlib.pyplot as plt
from pynauty import graph

from graphgen import generate_graph_degree
import pickle, requests, json, ast

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

print("Encoded username- {}".format(encoded_un))
print("Encoded password- {}".format(encoded_pw))
print('Encoded username||password = {}\n'.format(encoded))
# print('Length of encoding = {}\n'.format(len(encoded)))
# g = generate_graph_repeat_conn(encoded)
# g = generate_graph_skip(encoded)

g1 = generate_graph_degree(encoded, degree=16)
# print(f"Constructed graph G1 with {len(g1.nodes)} vertices and {len(g1.edges)} edges")

adj_dict_g1 = nx.to_dict_of_lists(g1)
# print(adj_dict_g1)
png_g1 = graph.Graph(len(adj_dict_g1), adjacency_dict=adj_dict_g1)
generators, _, _, _, _ = graph.autgrp(png_g1)

# if len(generators)>
# print(f"Found {len(generators)} isomorphisms\n{generators}")
g1_vertex_seq = g1.nodes
g2_vertex_seq = generators[-1]

g1_to_g2_map = {k:v for (k,v) in zip(g1_vertex_seq, g2_vertex_seq)}
print("G1 vertex seq-{}\n".format(g1_vertex_seq))
print("G2 vertex seq-{}\n".format(g2_vertex_seq))
print("Mapping from G1 to G2- {}\n".format(g1_to_g2_map))

g2 = nx.relabel_nodes(g1, mapping=g1_to_g2_map, copy=True)
adj_dict_g2 = nx.to_dict_of_lists(g2)


g1_adj_encoded = b64encode(pickle.dumps(adj_dict_g1)).decode('utf-8')
g2_adj_encoded = b64encode(pickle.dumps(adj_dict_g2)).decode('utf-8')

# print(pickle.loads(b64decode(g1_adj_encoded.encode('utf-8'))))




# dummy registration request

payload = {'username':username, 'G1':g1_adj_encoded, 'G2':g2_adj_encoded}
headers = {'Content-type': 'application/json'}


response = requests.post(url="http://127.0.0.1:5000/register", data=json.dumps(payload), headers=headers)

# print(pickle.loads(b64decode(response.text.encode('utf-8'))))

print(response.text)