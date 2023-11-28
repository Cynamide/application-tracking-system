from flask import Request
def getUseridFromtoken(request:Request)-> str:
    """
    Evaluates user id from the request header

    :return: string
    """
    headers = request.headers
    token = headers["Authorization"].split(" ")[1]
    userid = token.split(".")[0]
    return userid
