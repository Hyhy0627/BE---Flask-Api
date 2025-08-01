from flask import Blueprint

bp = Blueprint('test', __name__)

@bp.route('/')
def home():
    return {'message': 'Hello from Flask!'}
