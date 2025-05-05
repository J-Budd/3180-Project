from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()  # Initialize without app first
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:8080"])
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)  # Now associate with app and db
    login_manager.init_app(app)
    login_manager.login_view = 'api_login'

    from app.models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    from app import views
    from app import models

    return app