from create_app import create_app
from infrastructure.databases.extensions import db
from infrastructure.models.user.user import User

app = create_app()

def init_db():
    """Initialize the database with tables and initial data"""
    with app.app_context():
        # Tạo tất cả các bảng trong database
        db.create_all()
        print("Tất cả các bảng đã được tạo thành công!")
        
        # Kiểm tra và tạo admin user nếu chưa tồn tại
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(email="admin@example.com", role="admin")
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Đã tạo tài khoản admin mặc định!")

if __name__ == '__main__':
    init_db()
