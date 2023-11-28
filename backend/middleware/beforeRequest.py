from flask import Request,jsonify
from typing import List
import os
from datetime import datetime, timedelta

def delete_auth_token(token_to_delete: str, user_id: str, Users):
    """
    Deletes authorization token of the given user from the database

    :param token_to_delete: token to be deleted
    :param user_id: user id of the current active user
    :return: string
    """
    user = Users.objects(id=user_id).first()
    auth_tokens = []
    for token in user["authTokens"]:
        if token != token_to_delete:
            auth_tokens.append(token)
    user.update(authTokens=auth_tokens)

def beforeRequestMiddleware(request: Request,existing_endpoints: List[str],Users):
    try:
        # need to check the root part of the route, applications,resume and recommanded are protected
        if request.path.split(os.path.sep)[1] in existing_endpoints:
            headers = request.headers
            try:
                token = headers["Authorization"].split(" ")[1]
            except:
                return jsonify({"error": "Unauthorized"}), 401
            userid = token.split(".")[0]
            user = Users.objects(id=userid).first()

            if user is None:
                return jsonify({"error": "Unauthorized"}), 401

            expiry_flag = False
            for tokens in user["authTokens"]:
                if tokens["token"] == token:
                    expiry = tokens["expiry"]
                    expiry_time_object = datetime.strptime(
                        expiry, "%m/%d/%Y, %H:%M:%S"
                    )
                    if datetime.now() <= expiry_time_object:
                        expiry_flag = True
                    else:
                        delete_auth_token(tokens, userid,Users)
                    break

            if not expiry_flag:
                return jsonify({"error": "Unauthorized"}), 401

    except:
        return jsonify({"error": "Internal server error"}), 500

