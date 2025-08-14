from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db, Contact
from forms import ContactForm

# HTML routes
main = Blueprint("main", __name__)

@main.route("/")
def index():
    contacts = Contact.query.all()
    return render_template("index.html", contacts=contacts)

@main.route("/add", methods=["GET", "POST"])
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(contact)
        db.session.commit()
        flash("Contact added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add_contact.html", form=form)

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.phone = form.phone.data
        contact.email = form.email.data
        contact.address = form.address.data
        db.session.commit()
        flash("Contact updated successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("edit_contact.html", form=form)

@main.route("/delete/<int:id>")
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted!", "danger")
    return redirect(url_for("main.index"))


# Postman API routes
api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "phone": c.phone,
        "email": c.email,
        "address": c.address
    } for c in contacts])

@api.route("/contacts/<int:id>", methods=["GET"])
def get_contact(id):
    c = Contact.query.get_or_404(id)
    return jsonify({
        "id": c.id,
        "name": c.name,
        "phone": c.phone,
        "email": c.email,
        "address": c.address
    })

@api.route("/contacts", methods=["POST"])
def add_contact_api():
    data = request.json
    c = Contact(
        name=data["name"],
        phone=data["phone"],
        email=data["email"],
        address=data.get("address", "")
    )
    db.session.add(c)
    db.session.commit()
    return jsonify({"message": "Contact added", "id": c.id}), 201

@api.route("/contacts/<int:id>", methods=["PUT"])
def update_contact_api(id):
    data = request.json
    c = Contact.query.get_or_404(id)
    c.name = data.get("name", c.name)
    c.phone = data.get("phone", c.phone)
    c.email = data.get("email", c.email)
    c.address = data.get("address", c.address)
    db.session.commit()
    return jsonify({"message": "Contact updated"})

@api.route("/contacts/<int:id>", methods=["DELETE"])
def delete_contact_api(id):
    c = Contact.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"message": "Contact deleted"})
