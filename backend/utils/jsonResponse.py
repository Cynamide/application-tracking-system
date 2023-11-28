from flask import jsonify

def jsonResponse(message: str, statusNumber: int):
        return jsonify({"message": message}), statusNumber
