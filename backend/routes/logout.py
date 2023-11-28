from flask import jsonify
from backend.utils.userIdFromtoken import getUseridFromtoken 
from backend.utils.tokenFromHeader import tokenFromHeader
from flask import Request


def logoutRoute(request:Request, Users):
    """
    Logs out the user and deletes the existing token from the database

    :return: JSON object with status and message
    """
    try:
        userid = getUseridFromtoken(request)
        user = Users.objects(id=userid).first()
        auth_tokens = []
        incoming_token = tokenFromHeader(request)
        for token in user["authTokens"]:
            if token["token"] != incoming_token:
                auth_tokens.append(token)
        user.update(authTokens=auth_tokens)

        return jsonify({"success": ""}), 200

    except exception as error:
        print(error)
        return jsonify({"error": "Internal server error"}), 500


