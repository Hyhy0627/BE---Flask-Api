from infrastructure.databases.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from domain.models.user.user import User as DomainUser

class User(db.Model):
    """Database model for user"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")  # admin, tutor, student
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_domain(self):
        """Convert to domain model"""
        return DomainUser(
            id=self.id,
            email=self.email,
            password_hash=self.password_hash,
            role=self.role # truyền role sang domain model
        )
    
    @classmethod
    def from_domain(cls, domain_user):
        """Create from domain model"""
        return cls(
            id=domain_user.id,
            email=domain_user.email,
            password_hash=domain_user.password_hash,
            role=domain_user.role  # truyền role từ domain model
        )
