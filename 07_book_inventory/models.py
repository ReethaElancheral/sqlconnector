from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    published_year = db.Column(db.Integer)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # create SQLite DB locally

    return app
