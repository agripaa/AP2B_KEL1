import json
import jwt
import datetime
from models.user_model import add_user, get_user_by_username, get_user_by_email

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"


def register_user(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not (username and email and password):
        return {"message": "Missing fields"}, 400

    if get_user_by_username(username) or get_user_by_email(email):
        return {"message": "Username or email already exists"}, 400

    new_user = {
        "username": username,
        "email": email,
        "password": password,
    }
    add_user(new_user)

    return {"message": "User registered successfully"}, 201


def login_user(data):
    username = data.get("username")
    password = data.get("password")

    user = get_user_by_username(username)
    if user and user["password"] == password:
        token = generate_token(username)
        return {"token": token}, 200

    return {"message": "Invalid username or password"}, 400


def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
