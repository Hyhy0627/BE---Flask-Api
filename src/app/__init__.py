from flask import Flask
from app.extensions import db, jwt, ma

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.test import bp as test_bp
    app.register_blueprint(test_bp)

    return app
