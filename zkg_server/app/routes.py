import random

from flask import request

from . import app
from . import cache
from . import db
from .graph import graph


@app.route("/register", methods=["POST"])
def register():
    payload = request.get_json()
    collection = db["user_data"]

    if collection.find_one({"username": payload["username"]}) is not None:
        print(collection.find_one({"username": payload["username"]}))
        return {"message": "User already registered"}, 400

    result = collection.insert_one(payload)
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
        return {"message": f"{payload['username']} not found"}, 404

    cache.update(payload["username"], payload["h"])

    return {"b": random.randint(1, 2)}, 200


@app.route("/verify", methods=["POST"])
def verify():
    payload = request.get_json()
    collection = db["user_data"]

    user = collection.find_one({"username": payload["username"]})

    if user is None:
        return {"message": f"{payload['username']} not found"}, 404

    g2 = user["G2"]
    user_cache = cache.get(payload["username"])

    h = graph.build_graph(user_cache["h"])
    remapped_graph = graph.apply_isomorphic_mapping(h, payload["chi"])
    g2 = graph.build_graph(g2)

    print(remapped_graph)
    print(g2)
    if remapped_graph == g2:
        if user_cache["round"] == 10:
            status = "success"
            cache.delete(payload["username"])
        else:
            status = "pending"
        return {"status": status}, 200
    else:
        cache.delete(payload["username"])
        return {"status": "failure"}, 401
