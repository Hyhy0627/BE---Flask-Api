from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """User domain model representing a user in the system"""
    
    def __init__(self, id=None, email=None, password_hash=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
