from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    workouts = db.relationship("Workout", backref="owner", lazy=True)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_type = db.Column(db.String(100), nullable=False)
    steps = db.Column(db.Integer, default=0)
    hours = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
