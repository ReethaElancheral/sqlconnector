from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)  # UTC-compliant

    def __repr__(self):
        return f"<User {self.name}>"
