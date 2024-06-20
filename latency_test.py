from timeit import timeit

import requests
from faker import Faker

from zerok.client import ZKClient
from zerok.graphiso import GraphIsomorphism


fake = Faker()
problem = GraphIsomorphism()
server_url = "http://127.0.0.1:5000"
client = ZKClient(problem=problem, server_url=server_url)


def traditional_flow():
    username, password = fake.email(), fake.password(length=16)
    resp = requests.post(
        f"{server_url}/register_traditional",
        json={"username": username, "password": password},
    )
    resp.raise_for_status()

    resp = requests.post(
        f"{server_url}/login_traditional",
        json={"username": username, "password": password},
    )
    resp.raise_for_status()


def zk_flow():
    username, password = fake.email(), fake.password(length=16)
    ok, resp = client.register_user(username, password)
    if not ok:
        print(resp)
        return
    ok, resp = client.login_user(username, password)
    if not ok:
        print(resp)


print(timeit(traditional_flow, number=100), "ms")
print(timeit(zk_flow, number=100), "ms")
