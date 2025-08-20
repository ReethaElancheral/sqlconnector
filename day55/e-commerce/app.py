from flask import Flask
from config import Config
from models import db, login_manager
from flask_wtf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    CSRFProtect(app)

    # Blueprints
    from routes import main_bp, auth_bp, admin_bp
    from api import api_bp, csrf_exempt_bp

    # Exempt API (JSON) from CSRF so Fetch works easily
    csrf_exempt_bp(app)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    # Context processors (e.g., cart count)
    @app.context_processor
    def inject_globals():
        from flask_login import current_user
        from models import CartItem
        count = 0
        if current_user.is_authenticated:
            count = db.session.query(db.func.coalesce(db.func.sum(CartItem.quantity), 0)).filter_by(user_id=current_user.id).scalar()
        return {"cart_item_count": int(count)}

    return app

# For gunicorn: "gunicorn -w 2 -b 0.0.0.0:8000 app:app"
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
