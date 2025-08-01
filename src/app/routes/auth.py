from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.schemas.user_schema import UserSchema

# Khởi tạo Blueprint với prefix "/auth"
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Schema để serialize user khi trả về JSON
user_schema = UserSchema()

# ĐĂNG KÝ NGƯỜI DÙNG MỚI

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Kiểm tra nếu email đã tồn tại
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email đã được sử dụng'}), 400

    # Tạo user mới
    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user), 201

# ĐĂNG NHẬP

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    # Kiểm tra tài khoản hoặc mật khẩu sai
    if not user or not user.check_password(password):
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
    user = User.query.get(user_id)

    return jsonify(user_schema.dump(user))