from flask import Flask
from models import db
from routes import main
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # creates SQLite DB locally or uses DATABASE_URL if set

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
