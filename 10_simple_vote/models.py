from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100), nullable=False)
    votes = db.relationship('Vote', backref='candidate', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_name = db.Column(db.String(100), nullable=False, unique=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)

def create_app():
    from config import Config
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes import main, api
    app.register_blueprint(main)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()  # creates SQLite DB locally

    return app
