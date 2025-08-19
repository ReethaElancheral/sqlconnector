import os
from flask import Flask, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Product
from forms import LoginForm, ProductForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "fallback-secret")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "instance", "ecommerce.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------- Routes ----------------

@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_admin:
            login_user(user)
            flash("Logged in as admin!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials or not an admin.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("index"))
    products = Product.query.all()
    return render_template("dashboard.html", products=products)

@app.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("index"))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data, price=form.price.data)
        db.session.add(product)
        db.session.commit()
        flash("Product added!", "success")
        return redirect(url_for("dashboard"))
    return render_template("add_product.html", form=form)

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("index"))
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        db.session.commit()
        flash("Product updated!", "success")
        return redirect(url_for("dashboard"))
    return render_template("edit_product.html", form=form)

@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash("Access denied.", "danger")
        return redirect(url_for("index"))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted!", "success")
    return redirect(url_for("dashboard"))

# ---------------- Run App ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(email="admin@gmail.com").first():
            hashed_pw = bcrypt.generate_password_hash("admin1234").decode("utf-8")
            admin = User(email="admin@gmail.com", password=hashed_pw, is_admin=True)
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
