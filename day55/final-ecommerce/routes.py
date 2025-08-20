from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Product, CartItem

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/products')
def products():
    items = Product.query.all()
    return render_template('products.html', products=items)

@main_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(item)
    db.session.commit()
    flash('Product added to cart!', 'success')
    return redirect(url_for('main.products'))

@main_bp.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum([item.quantity * item.product.price for item in items])
    return render_template('cart.html', items=items, total=total)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists', 'danger')
        else:
            user = User(username=request.form['username'], email=request.form['email'])
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
            flash('Registration successful', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))