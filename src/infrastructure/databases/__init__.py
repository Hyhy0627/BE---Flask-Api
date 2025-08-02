from infrastructure.databases.extensions import db, jwt, ma
from infrastructure.databases.mssql import init_mssql, Base

def init_db(app):
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize MSSQL (if needed)
    init_mssql(app)
    
    # Initialize JWT and Marshmallow
    jwt.init_app(app)
    ma.init_app(app)