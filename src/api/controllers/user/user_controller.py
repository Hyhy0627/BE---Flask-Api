from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from infrastructure.models.user.user import User
from services.user_service import UserService
from api.schemas.user_schema import UserSchema
from infrastructure.databases.base import db
from api.middleware import role_required

# Khởi tạo Blueprint với prefix "/auth"
user_bp = Blueprint('api', __name__)

# Service và Schema
user_service = UserService()
user_schema = UserSchema()

@user_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')  # Chỉ admin mới được xem danh sách user
def list_users():
    users = User.query.all()
    return jsonify(users=[{"id": u.id,
                        #    "username": u.username,
                           "email": u.email, "role": u.role } for u in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):

    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))

@user_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.json
    # Only extract expected fields
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # default role if not provided

    if not email or not password:
        return jsonify(msg="Missing email or password"), 400
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify(msg="User with this email already exists"), 400

    try:
        user = user_service.create_user(email=email, password=password, role=role)

        return jsonify(user_schema.dump(user)), 201
    except Exception as e:
        return jsonify(msg=str(e)), 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(msg="User deleted")

# CẬP NHẬT THÔNG TIN NGƯỜI DÙNG
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    if current_user_id != user_id:
        return jsonify(msg="Unauthorized"), 403

    user = User.query.get_or_404(user_id)
    data = request.json

    # if 'username' in data:
    #     if User.query.filter(User.username == data['username'], User.id != user_id).first():
    #         return jsonify(msg="Username already taken"), 400
    #     user.username = data['username']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(msg="User updated", user={"id": user.id, "username": user.username})
