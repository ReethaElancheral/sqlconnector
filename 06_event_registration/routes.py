from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Attendee

main = Blueprint("main", __name__)

@main.route("/")
def index():
    attendees = Attendee.query.all()
    return render_template("index.html", attendees=attendees)

@main.route("/add", methods=["GET", "POST"])
def add_attendee():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        event_name = request.form['event_name']
        attendee = Attendee(name=name, email=email, event_name=event_name)
        db.session.add(attendee)
        db.session.commit()
        flash("Attendee added successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template("add_attendee.html")

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_attendee(id):
    attendee = Attendee.query.get_or_404(id)
    if request.method == "POST":
        attendee.name = request.form['name']
        attendee.email = request.form['email']
        attendee.event_name = request.form['event_name']
        db.session.commit()
        flash("Attendee updated successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template("edit_attendee.html", attendee=attendee)

@main.route("/delete/<int:id>")
def delete_attendee(id):
    attendee = Attendee.query.get_or_404(id)
    db.session.delete(attendee)
    db.session.commit()
    flash("Attendee deleted!", "danger")
    return redirect(url_for('main.index'))
