import os
from flask import Flask, render_template, redirect, url_for, flash, request
from extensions import db, bcrypt, login_manager
from flask_login import login_user, login_required, logout_user, current_user

# -------------------- Flask App --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "fallback-local-secret")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_folder = os.environ.get("DB_FOLDER", os.path.join(BASE_DIR, "instance"))
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, "notes.db")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(BASE_DIR, "instance", "notes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from models import User, Note
from forms import RegisterForm, LoginForm, NoteForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- Routes --------------------
@app.route("/")
def index():
    return render_template("index.html")

# Register
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
        flash("Account created! You can now login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Welcome {current_user.username}!", "success")
            return redirect(url_for("notes"))
        else:
            flash("Login failed. Check email/password.", "danger")
    return render_template("login.html", form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))

# Notes
@app.route("/notes")
@login_required
def notes():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=user_notes)

# Add note
@app.route("/notes/add", methods=["GET", "POST"])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash("Note added successfully!", "success")
        return redirect(url_for("notes"))
    return render_template("edit_note.html", form=form, action="Add")

# Edit note
@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("You cannot edit this note.", "danger")
        return redirect(url_for("notes"))
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash("Note updated successfully!", "success")
        return redirect(url_for("notes"))
    return render_template("edit_note.html", form=form, action="Edit")

# Delete note
@app.route("/notes/<int:note_id>/delete")
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        flash("You cannot delete this note.", "danger")
        return redirect(url_for("notes"))
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted!", "info")
    return redirect(url_for("notes"))

# -------------------- Run App --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
