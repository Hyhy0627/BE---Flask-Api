from domain.models.user import User
from infrastructure.repositories.user_repository import UserRepository

class UserService:
    """Service for user-related operations"""
    
    def __init__(self, user_repository=None):
        self.repository = user_repository or UserRepository()
    
    def get_user_by_id(self, user_id):
        """Get a user by ID"""
        return self.repository.get_by_id(user_id)
    
    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.repository.get_by_email(email)
    
    def create_user(self, email, password):
        """Create a new user"""
        user = User(email=email)
        user.set_password(password)
        return self.repository.create(user)
    
    def authenticate_user(self, email, password):
        """Authenticate a user"""
        user = self.repository.get_by_email(email)
        if user and user.check_password(password):
            return user
        return None
