import os
from flask import Flask, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt, login_manager
from flask_login import login_user, login_required, logout_user, current_user

# -------------------- Flask App Setup --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "fallback-local-secret")


# Windows-safe absolute path for SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_folder = os.path.join(BASE_DIR, "instance")
os.makedirs(db_folder, exist_ok=True)  # ensure instance folder exists
db_path = os.path.join(db_folder, "tasks.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# -------------------- Import models AFTER db init --------------------
from models import User, Task
from forms import RegisterForm, LoginForm, TaskForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- Routes --------------------
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
        flash("Account created successfully! You can now login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Logged in successfully!", "success")
            return redirect(url_for("tasks"))
        else:
            flash("Login failed. Check email/password.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, due_date=form.due_date.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Task added!", "success")
        return redirect(url_for("tasks"))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("tasks.html", form=form, tasks=tasks)

@app.route("/task/<int:task_id>/delete")
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You cannot delete this task.", "danger")
        return redirect(url_for("tasks"))
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "info")
    return redirect(url_for("tasks"))

@app.route("/task/<int:task_id>/complete")
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash("You cannot update this task.", "danger")
        return redirect(url_for("tasks"))
    task.completed = True
    db.session.commit()
    flash("Task marked as completed!", "success")
    return redirect(url_for("tasks"))

# -------------------- Run App --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables automatically
    app.run(debug=True)
