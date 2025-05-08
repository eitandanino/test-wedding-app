from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user  # Import necessary modules
from flask_migrate import Migrate

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize Flask-Migrate
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Migrate with the app and db
    migrate.init_app(app, db)

    login_manager = LoginManager()  # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Set the login view (important!)

    from app.models import User  # Import your User model (important!)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Convert user_id to int (important!)

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)  # This is what makes current_user available

    from app.routes import bp
    app.register_blueprint(bp)

    return app
