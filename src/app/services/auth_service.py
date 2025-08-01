from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(email, password):
    if User.query.filter_by(email=email).first():
        return None, "Email đã được sử dụng"
    
    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None
