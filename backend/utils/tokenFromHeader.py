from flask import Request

def tokenFromHeader(request: Request)-> str:
    """
    Evaluates token from the request header

    :return: string
    """
    headers = request.headers
    token = headers["Authorization"].split(" ")[1]
    return token 
