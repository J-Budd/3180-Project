from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    photo = db.Column(db.String(255), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    parish = db.Column(db.String(255), nullable=True)
    biography = db.Column(db.String, nullable=True)
    sex = db.Column(db.String(10), nullable=True)
    race = db.Column(db.String(10), nullable=True)
    birth_year = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)
    fav_cuisine = db.Column(db.String(255), nullable=True)
    fav_color = db.Column(db.String(50), nullable=True)
    fav_school_subject = db.Column(db.String(255), nullable=True)
    political = db.Column(db.Boolean, nullable=True)
    religion = db.Column(db.String(255), nullable=True)
    family_oriented = db.Column(db.Boolean, nullable=True)


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fav_user_id_fk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)