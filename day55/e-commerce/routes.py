from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Product, CartItem
from forms import RegisterForm, LoginForm, ProductForm

main_bp = Blueprint("main", __name__)
auth_bp = Blueprint("auth", __name__)
admin_bp = Blueprint("admin", __name__)

@main_bp.route("/")
def home():
    products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    return render_template("home.html", products=products)

@main_bp.route("/products")
def products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("products.html", products=products)

@main_bp.route("/cart")
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_cents = sum(item.product.price_cents * item.quantity for item in items)
    return render_template("cart.html", items=items, total_cents=total_cents)

# ---------- Auth ----------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first():
            flash("Email or username already exists", "danger")
            return render_template("register.html", form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Welcome back!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.home"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("main.home"))

# ---------- Admin: Product CRUD ----------
def admin_required():
    return current_user.is_authenticated and current_user.is_admin

@admin_bp.before_request
def restrict_admin():
    if request.endpoint and request.blueprint == "admin":
        # Allow only authenticated admins
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for("auth.login"))

@admin_bp.route("/products")
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("admin_products.html", products=products)

@admin_bp.route("/products/new", methods=["GET", "POST"])
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(
            name=form.name.data,
            description=form.description.data,
            price_cents=form.price_cents.data,
            image_url=form.image_url.data or None,
        )
        db.session.add(p)
        db.session.commit()
        flash("Product created", "success")
        return redirect(url_for("admin.admin_products"))
    return render_template("product_form.html", form=form, title="Create Product")

@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash("Product updated", "success")
        return redirect(url_for("admin.admin_products"))
    return render_template("product_form.html", form=form, title="Edit Product")

@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    flash("Product deleted", "info")
    return redirect(url_for("admin.admin_products"))
