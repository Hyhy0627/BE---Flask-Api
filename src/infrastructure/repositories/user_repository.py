from infrastructure.databases.extensions import db
from infrastructure.models.user.user import User
from domain.models.user import User as DomainUser

class UserRepository:
    """Repository for user data access"""
    
    def get_by_id(self, user_id):
        """Get user by ID"""
        user = User.query.get(user_id)
        return user.to_domain() if user else None
    
    def get_by_email(self, email):
        """Get user by email"""
        user = User.query.filter_by(email=email).first()
        return user.to_domain() if user else None
    
    def create(self, domain_user):
        """Create a new user"""
        user = User.from_domain(domain_user)
        db.session.add(user)
        db.session.commit()
        return user.to_domain()
    
    def update(self, domain_user):
        """Update an existing user"""
        user = User.query.get(domain_user.id)
        if user:
            user.email = domain_user.email
            user.password_hash = domain_user.password_hash
            db.session.commit()
            return user.to_domain()
        return None
    
    def delete(self, user_id):
        """Delete a user"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
