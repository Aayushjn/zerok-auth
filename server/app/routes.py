from app import app
from flask import request, jsonify
from app import db


@app.route("/")
@app.route("/register", methods=["POST"])
def register():

    payload = request.json

    collection = db["user_data"]
    
    result = collection.insert_one({'username': payload['username'], 'G1': payload['G1'], 'G2': payload['G2'] })
    if not result.inserted_id:
        return {"message": "Failed to register user"}, 500
    else:
        return {"message": "Registration Successful", }, 200

    # return payload
