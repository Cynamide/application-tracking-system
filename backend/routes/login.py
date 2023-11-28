from flask import Request,jsonify
import json,uuid
from datetime import datetime, timedelta
import hashlib

def loginRoute(request: Request,Users):
    """
    Logs in the user and creates a new authorization token and stores in the database

    :return: JSON object with status and message
    """
    try:
        try:
            data = json.loads(request.data)
            _ = data["username"]
            _ = data["password"]
        except:
            return jsonify({"error": "Username or password missing"}), 400
        password_hash = hashlib.md5(data["password"].encode()).hexdigest()
        print(data,"user data from request",password_hash)
        print(Users)
        user = Users.objects(
            username=data["username"], password=password_hash
        ).first()
        if user is None:
            return jsonify({"error": "Wrong username or password"})
        token = str(user["id"]) + "." + str(uuid.uuid4())
        expiry = datetime.now() + timedelta(days=1)
        expiry_str = expiry.strftime("%m/%d/%Y, %H:%M:%S")
        auth_tokens_new = user["authTokens"] + [
            {"token": token, "expiry": expiry_str}
        ]
        user.update(authTokens=auth_tokens_new)
        return jsonify({"token": token, "expiry": expiry_str})
    except exception as error:
        print("error is: ",error)
        return jsonify({"error": "Internal server error"}), 500 
