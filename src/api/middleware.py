# Middleware functions for processing requests and responses

from flask import request, jsonify
from flask_cors import CORS
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from services.user_service import UserService

def log_request_info(app):
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

def handle_options_request():
    return jsonify({'message': 'CORS preflight response'}), 200

def error_handling_middleware(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response

def add_custom_headers(response):
    response.headers['X-Custom-Header'] = 'Value'
    return response

def setup_middleware(app):
    # Initialize CORS
    CORS(app)
    
    @app.before_request
    def before_request():
        log_request_info(app)

    @app.after_request
    def after_request(response):
        return add_custom_headers(response)

    @app.errorhandler(Exception)
    def handle_exception(error):
        return error_handling_middleware(error)

    @app.route('/options', methods=['OPTIONS'])
    def options_route():
        return handle_options_request()

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = UserService().get_user_by_id(user_id)
            if not user or user.role != required_role:
                return {'message': 'Forbidden'}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator