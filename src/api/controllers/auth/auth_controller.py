from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from infrastructure.models.user.user import User
from services.user_service import UserService
from api.schemas.user_schema import UserSchema
from infrastructure.databases.base import db

# Khởi tạo Blueprint với prefix "/auth"
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Service và Schema
user_service = UserService()
user_schema = UserSchema()

# ĐĂNG KÝ NGƯỜI DÙNG MỚI
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')
    # Kiểm tra nếu email đã tồn tại
    if user_service.get_user_by_email(email):
        return jsonify({'message': 'Email đã được sử dụng'}), 400

    # Tạo user mới
    user = user_service.create_user(email, password, role)

    return user_schema.dump(user), 201

# ĐĂNG NHẬP
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = user_service.authenticate_user(email, password)

    # Kiểm tra tài khoản hoặc mật khẩu sai
    if not user:
        return jsonify({'message': 'Tài khoản hoặc mật khẩu không đúng'}), 401

    # Tạo token chứa user ID
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user_schema.dump(user)
    })

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=str(user_id))
    return jsonify({'access_token': new_access_token})

# LẤY THÔNG TIN USER HIỆN TẠI
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    # Lấy ID từ token
    user_id = get_jwt_identity()

    # Truy vấn user từ DB
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        return jsonify({'message': 'User không tồn tại'}), 404

    return jsonify(user_schema.dump(user))
