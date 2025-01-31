"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)


# Allow CORS requests to this API
CORS(api)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@api.route("/login", methods=["POST"])
def login():
    emailBody = request.json.get("email", None)
    passwordBody = request.json.get("password", None)
    existing_user = User.query.filter_by(email = emailBody).first()
    if not existing_user:
        return jsonify({"msg": "Bad email or password"}), 401
    if not check_password_hash(existing_user.password, passwordBody):
        return jsonify({"msg": "Bad email or password"}), 401
    
    access_token = create_access_token(identity = emailBody)
    return jsonify(access_token=access_token)


@api.route("/signup", methods=["POST"])
def signup():
    emailBody = request.json.get("email", None)
    passwordBody = request.json.get("password", None)
    newUser = User(email = emailBody, password = generate_password_hash(passwordBody), is_active = True)
    db.session.add(newUser)
    db.session.commit()

    return jsonify("User was created"), 200


@api.route("/hello", methods=["GET"])
@jwt_required()
def get_hello():

    emailBody = get_jwt_identity(),
    dictionary = {
        "message":"Hello: " + emailBody
    }
    
    return jsonify(dictionary)


