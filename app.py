from flask import Flask, jsonify, request
import requests
import sqlite3
import os 
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity 
from dotenv import load_dotenv
from flasgger import swag_from 

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify("")


app.run(debug=True)
