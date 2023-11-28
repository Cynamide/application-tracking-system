from flask import Request,jsonify
import json
import hashlib
from backend.utils.dbUtils import get_new_user_id 

def signupRoute(request: Request,Users):
    """
    Creates a new user profile and adds the user to the database and returns the message

    :return: JSON object
    """
    try:
        data = json.loads(request.data)
        print(data)
        try:
            _ = data["username"]
            _ = data["password"]
            _ = data["fullName"]
        except:
            return jsonify({"error": "Missing fields in input"}), 400

        username_exists = Users.objects(username=data["username"])
        if len(username_exists) != 0:
            return jsonify({"error": "Username already exists"}), 400
        password = data["password"]
        password_hash = hashlib.md5(password.encode())
        user = Users(
            id=get_new_user_id(Users),
            fullName=data["fullName"],
            username=data["username"],
            password=password_hash.hexdigest(),
            authTokens=[],
            applications=[],
        )
        user.save()
        return jsonify(user.to_json()), 200
    except exception as error:
        print(error)
        return jsonify({"error": "Internal server error"}), 500


