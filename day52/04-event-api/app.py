from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Event
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

api = Api(app)

# Helper function to validate date
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Resources
class EventListResource(Resource):
    def get(self):
        events = Event.query.all()
        return {"events": [e.to_dict() for e in events]}, 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "date" not in data or "location" not in data:
            return {"error": "Name, date, and location are required"}, 400
        if not is_valid_date(data["date"]):
            return {"error": "Date must be in YYYY-MM-DD format"}, 400

        new_event = Event(name=data["name"], date=data["date"], location=data["location"])
        db.session.add(new_event)
        db.session.commit()
        return new_event.to_dict(), 201

class EventResource(Resource):
    def get(self, id):
        event = Event.query.get(id)
        if not event:
            return {"error": "Event not found"}, 404
        return event.to_dict(), 200

    def put(self, id):
        event = Event.query.get(id)
        if not event:
            return {"error": "Event not found"}, 404

        data = request.get_json()
        if "name" in data:
            event.name = data["name"]
        if "date" in data:
            if not is_valid_date(data["date"]):
                return {"error": "Date must be in YYYY-MM-DD format"}, 400
            event.date = data["date"]
        if "location" in data:
            event.location = data["location"]

        db.session.commit()
        return event.to_dict(), 200

    def delete(self, id):
        event = Event.query.get(id)
        if not event:
            return {"error": "Event not found"}, 404
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}, 200

# Add resources
api.add_resource(EventListResource, "/events")
api.add_resource(EventResource, "/events/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
