from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models.user import User

def role_required(role_name):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role != role_name:
                return jsonify({"message": "Không có quyền"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
