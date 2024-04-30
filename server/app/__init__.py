from flask import Flask
from app.dbconnect import Connection

app = Flask(__name__)
db=Connection('zkp_users')

from app import routes
