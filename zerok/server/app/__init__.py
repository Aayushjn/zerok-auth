from flask import Flask

from .dbconnect import Connection

app = Flask(__name__)
db = Connection("zkp_users")

from . import routes
