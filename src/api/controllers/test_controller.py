from flask import Blueprint

# Khởi tạo Blueprint
test_bp = Blueprint('test', __name__)

@test_bp.route('/')
def home():
    return {'message': 'Hello from Flask Clean Architecture!'}
