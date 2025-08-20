from flask import Flask
from config import Config
from models import db, login_manager, Product, User, CartItem
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    CSRFProtect(app)

    from routes import main_bp, auth_bp
    from api import api_bp, csrf_exempt_bp

    csrf_exempt_bp(app)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")

    with app.app_context():
        db.create_all()
        seed_products()

    return app

def seed_products():
    if Product.query.count() == 0:
        demo_products = [
            Product(name="Meditation Book", price=1999, description="A guide to inner peace and mindfulness."),
            Product(name="Yoga Mat", price=2500, description="Comfortable non-slip mat for daily practice."),
            Product(name="Aromatherapy Candle", price=1550, description="Lavender-scented candle for relaxation."),
            Product(name="Essential Oil Set", price=2999, description="Set of 5 pure essential oils for wellness."),
            Product(name="Mindfulness Journal", price=1200, description="Track your thoughts, progress, and gratitude."),
            Product(name="Herbal Tea Pack", price=1050, description="Organic calming teas for stress relief.")
        ]
        db.session.add_all(demo_products)
        db.session.commit()
        print("✅ Demo products added automatically!")

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)