from domain.models.user.user import User as DomainUser

class User(DomainUser):
    """User domain model"""
    
    def __init__(self, id=None, email=None, password_hash=None):
        super().__init__(id, email, password_hash)
