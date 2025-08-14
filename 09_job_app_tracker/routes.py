from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db, Application
from forms import ApplicationForm

# HTML routes
main = Blueprint("main", __name__)

@main.route("/")
def index():
    status_filter = request.args.get('status')
    if status_filter:
        applications = Application.query.filter_by(status=status_filter).all()
    else:
        applications = Application.query.all()
    return render_template("index.html", applications=applications)

@main.route("/add", methods=["GET", "POST"])
def add_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        app_entry = Application(
            name=form.name.data,
            email=form.email.data,
            job_title=form.job_title.data,
            status=form.status.data
        )
        db.session.add(app_entry)
        db.session.commit()
        flash("Application added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add_application.html", form=form)

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    app_entry = Application.query.get_or_404(id)
    form = ApplicationForm(obj=app_entry)
    if form.validate_on_submit():
        app_entry.name = form.name.data
        app_entry.email = form.email.data
        app_entry.job_title = form.job_title.data
        app_entry.status = form.status.data
        db.session.commit()
        flash("Application updated!", "success")
        return redirect(url_for("main.index"))
    return render_template("edit_application.html", form=form)

@main.route("/delete/<int:id>")
def delete_application(id):
    app_entry = Application.query.get_or_404(id)
    db.session.delete(app_entry)
    db.session.commit()
    flash("Application deleted!", "danger")
    return redirect(url_for("main.index"))


# Postman API routes
api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/applications", methods=["GET"])
def get_applications():
    status_filter = request.args.get('status')
    if status_filter:
        applications = Application.query.filter_by(status=status_filter).all()
    else:
        applications = Application.query.all()
    return jsonify([{
        "id": a.id,
        "name": a.name,
        "email": a.email,
        "job_title": a.job_title,
        "status": a.status
    } for a in applications])

@api.route("/applications/<int:id>", methods=["GET"])
def get_application(id):
    a = Application.query.get_or_404(id)
    return jsonify({
        "id": a.id,
        "name": a.name,
        "email": a.email,
        "job_title": a.job_title,
        "status": a.status
    })

@api.route("/applications", methods=["POST"])
def add_application_api():
    data = request.json
    a = Application(
        name=data["name"],
        email=data["email"],
        job_title=data["job_title"],
        status=data.get("status", "applied")
    )
    db.session.add(a)
    db.session.commit()
    return jsonify({"message": "Application added", "id": a.id}), 201

@api.route("/applications/<int:id>", methods=["PUT"])
def update_application_api(id):
    data = request.json
    a = Application.query.get_or_404(id)
    a.name = data.get("name", a.name)
    a.email = data.get("email", a.email)
    a.job_title = data.get("job_title", a.job_title)
    a.status = data.get("status", a.status)
    db.session.commit()
    return jsonify({"message": "Application updated"})

@api.route("/applications/<int:id>", methods=["DELETE"])
def delete_application_api(id):
    a = Application.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"message": "Application deleted"})
