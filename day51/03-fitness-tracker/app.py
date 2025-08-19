import os
from flask import Flask, render_template, redirect, url_for, flash, request, session
from extensions import db, bcrypt, login_manager
from flask_login import login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "fallback-secret")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_folder = os.path.join(BASE_DIR, "instance")
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "fitness.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "instance", "fitness.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from models import User, Workout
from forms import RegisterForm, LoginForm, WorkoutForm, ProfileForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if len(form.password.data) < 8:
            flash("Password must be at least 8 characters long", "danger")
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

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = WorkoutForm()
    if 'last_workout' in session:
        form.workout_type.data = session['last_workout']
    if form.validate_on_submit():
        workout = Workout(
            workout_type=form.workout_type.data,
            steps=form.steps.data,
            hours=form.hours.data,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()
        session['last_workout'] = form.workout_type.data
        flash("Workout logged successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("dashboard.html", form=form)

@app.route("/history")
@login_required
def history():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template("history.html", workouts=workouts)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for("profile"))
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.new_password.data:
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", form=form)

# ---------------- Run App ----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
