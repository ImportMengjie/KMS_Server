from flask import *
from  config import *
from model import *
from functools import wraps


def auth_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.json.get('token')
        if not token:
            return jsonify({json_success: False, json_msg: msg_auth_need}), HTTP_Forbidden
        u = User.objects(token=token).first()
        if not u:
            return jsonify({json_success: False, json_msg: msg_auth_require}), HTTP_Forbidden
        return func(user=u, *args, **kwargs)
    return wrapper