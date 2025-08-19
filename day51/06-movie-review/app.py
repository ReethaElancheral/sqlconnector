import os
from flask import Flask, render_template, redirect, url_for, flash
from extensions import db, bcrypt, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Review
from forms import RegisterForm, LoginForm, ReviewForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "fallback-secret")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "instance", "reviews.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- Routes ----------------
@app.route("/")
def index():
    reviews = Review.query.order_by(Review.date_posted.desc()).all()
    return render_template("index.html", reviews=reviews)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please login or use a different email.", "danger")
            return redirect(url_for("register"))
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome {current_user.username}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Login failed. Check email/password.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/add_review", methods=["GET", "POST"])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(movie_title=form.movie_title.data,
                        rating=form.rating.data,
                        comment=form.comment.data,
                        author=current_user)
        db.session.add(review)
        db.session.commit()
        flash("Review submitted successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("add_review.html", form=form)

# ---------------- Run App ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
