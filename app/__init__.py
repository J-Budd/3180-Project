from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from flask_cors import CORS  #Allows cross-origin requests/ frontend to back-end communication


db = SQLAlchemy()

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"]) # Enable CORS for the Flask app
app.config.from_object(Config)



db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import Users # Import your models here

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

from app import views
from app import models