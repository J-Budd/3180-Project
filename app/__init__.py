from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import Config

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)

from app import views