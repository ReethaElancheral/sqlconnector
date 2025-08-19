from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Contact
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)

# -------- Resources ----------
class ContactListResource(Resource):
    def get(self):
        contacts = Contact.query.all()
        return {"contacts": [c.to_dict() for c in contacts]}, 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "phone" not in data:
            return {"error": "Name and phone are required"}, 400

        if len(data["phone"]) != 10 or not data["phone"].isdigit():
            return {"error": "Phone number must be 10 digits"}, 400

        contact = Contact(
            name=data["name"],
            phone=data["phone"],
            email=data.get("email")
        )
        db.session.add(contact)
        db.session.commit()
        return {"message": "Contact created", "contact": contact.to_dict()}, 201


class ContactResource(Resource):
    def get(self, id):
        contact = Contact.query.get(id)
        if not contact:
            return {"error": "Contact not found"}, 404
        return {"contact": contact.to_dict()}, 200

    def put(self, id):
        contact = Contact.query.get(id)
        if not contact:
            return {"error": "Contact not found"}, 404

        data = request.get_json()
        if "name" in data:
            contact.name = data["name"]
        if "phone" in data:
            if len(data["phone"]) != 10 or not data["phone"].isdigit():
                return {"error": "Phone number must be 10 digits"}, 400
            contact.phone = data["phone"]
        if "email" in data:
            contact.email = data["email"]

        db.session.commit()
        return {"message": "Contact updated", "contact": contact.to_dict()}, 200

    def delete(self, id):
        contact = Contact.query.get(id)
        if not contact:
            return {"error": "Contact not found"}, 404
        db.session.delete(contact)
        db.session.commit()
        return {"message": "Contact deleted"}, 200


# -------- Routes ----------
api.add_resource(ContactListResource, "/contacts")
api.add_resource(ContactResource, "/contacts/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
