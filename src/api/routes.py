from api.controllers.todo_controller import bp as todo_bp
from api.controllers.auth.auth_controller import auth_bp
from api.controllers.test_controller import test_bp

def register_routes(app):
    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)