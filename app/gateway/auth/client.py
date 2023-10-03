from flask import request, make_response, jsonify
from functools import wraps
import jwt


from config import config


def authenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(token, config.secret_key, algorithms=['HS256'])
            # TODO(mirco): fetch user settings here if needed
        except Exception:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
        return f(*args, **kwargs)
    return decorator

