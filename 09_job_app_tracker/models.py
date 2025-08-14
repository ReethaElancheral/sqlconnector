from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="applied")  # applied, shortlisted, rejected

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes import main, api
    app.register_blueprint(main)
    app.register_blueprint(api)

    with app.app_context():
        db.create_all()  # creates SQLite DB locally

    return app
