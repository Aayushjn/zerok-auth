import json
import os
import random
from base64 import b64decode
from collections import Counter

import argon2
from flask import request

from . import app
from . import db
# from . import cache

# from .graph import graph

ph = argon2.PasswordHasher()


def format_dict_payload(s: str, parse_int_keys: bool = True) -> dict:
    d = json.loads(b64decode(s).decode())

    return {int(k): v for k, v in d.items()} if parse_int_keys else d


def compare_adj_lists(
    adj_list1: dict[int, list[int]], adj_list2: dict[int, list[int]]
) -> bool:
    def _compare_list(l1: list[int], l2: list[int]) -> bool:
        return Counter(l1) == Counter(l2)

    if len(adj_list1) != len(adj_list2):
        return False

    for v1, v2 in zip(adj_list1.values(), adj_list2.values()):
        if not _compare_list(v1, v2):
            return False

    return True


@app.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    collection = db["user_data"]

    if collection.find_one({"username": payload["username"]}) is not None:
        return {"message": "Username already registered"}, 400

    # db_data = {
    #     "username": payload["username"],
    #     "G1": format_dict_payload(payload["G1"], False),
    #     "G2": format_dict_payload(payload["G2"], False),
    # }

    db_data = {
        "username": payload["username"],
        "parameters": {},
    }

    for k, v in payload["parameters"].items():
        db_data["parameters"][k] = format_dict_payload(v, False)

    result = collection.insert_one(db_data)
    if not result.inserted_id:
        return {"message": "Failed to register user"}, 500
    else:
        return {"message": "Registration Successful"}, 200


@app.route("/register_traditional", methods=["POST"])
def register_traditional():
    payload = request.get_json()
    collection = db["user_data_traditional"]

    if collection.find_one({"username": payload["username"]}) is not None:
        return {"message": "Username already registered"}, 400

    salt = os.urandom(16)
    hashed_pw = ph.hash(password=payload["password"], salt=salt)

    db_data = {
        "username": payload["username"],
        "password": hashed_pw,
    }
    result = collection.insert_one(db_data)
    if not result.inserted_id:
        return {"message": "Failed to register user"}, 500
    else:
        return {"message": "Registration Successful"}, 200


@app.route("/login", methods=["POST"])
def login():
    payload = request.get_json()
    collection = db["user_data"]

    user = collection.find_one({"username": payload["username"]})

    if user is None:
        return {
            "status": "failure",
            "message": f"Username {payload['username']} not found",
        }, 404

    b = random.randint(1, 2)
    h = format_dict_payload(payload["h"])
    cache.update(payload["username"], h, b)

    return {"b": b}, 200


@app.route("/login_traditional", methods=["POST"])
def login_traditional():
    payload = request.get_json()
    collection = db["user_data_traditional"]

    user = collection.find_one({"username": payload["username"]})

    if user is None:
        return {
            "status": "failure",
            "message": f"Username {payload['username']} not found",
        }, 404

    stored_pw = user["password"]
    try:
        result = ph.verify(hash=stored_pw, password=payload["password"])
        if result:
            return {"status": "success"}, 200
    except (
        argon2.exceptions.VerificationError,
        argon2.exceptions.InvalidHashError,
    ) as e:
        return {"status": "failure", "message": str(e)}, 500


@app.route("/verify", methods=["POST"])
def verify():
    payload = request.get_json()
    collection = db["user_data"]

    user = collection.find_one({"username": payload["username"]})

    if user is None:
        return {"status": "failure", "message": f"{payload['username']} not found"}, 404

    user_cache = cache.get(payload["username"])
    h = graph.build_graph(user_cache["h"])
    chi = format_dict_payload(payload["chi"])
    remapped_graph = graph.apply_isomorphic_mapping(h, chi)
    remap_adj_list = graph.get_adjacency_list(remapped_graph)

    if user_cache["b"] == 1:
        g1_adj_list = {int(k): v for k, v in user["G1"].items()}
        if compare_adj_lists(remap_adj_list, g1_adj_list):
            round_successful = True
        else:
            round_successful = False
    else:
        g2_adj_list = {int(k): v for k, v in user["G2"].items()}
        if compare_adj_lists(remap_adj_list, g2_adj_list):
            round_successful = True
        else:
            round_successful = False

    if round_successful:
        if user_cache["round"] == 10:
            status = "success"
            cache.delete(payload["username"])
        else:
            status = "pending"
        return {"status": status}, 200
    else:
        cache.delete(payload["username"])
        return {"status": "failure", "message": "Login failed"}, 401
