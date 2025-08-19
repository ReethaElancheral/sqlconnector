import re
from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Feedback
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

class FeedbackListResource(Resource):
    def get(self):
        feedbacks = Feedback.query.all()
        return {"feedbacks": [fb.to_dict() for fb in feedbacks]}, 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "email" not in data or "message" not in data:
            return {"status": "error", "message": "name, email, and message are required"}, 400

        if not re.match(EMAIL_REGEX, data["email"]):
            return {"status": "error", "message": "Invalid email format"}, 400

        feedback = Feedback(name=data["name"], email=data["email"], message=data["message"])
        db.session.add(feedback)
        db.session.commit()

        return {
            "status": "success",
            "message": f"Thank you {data['name']} for your feedback!"
        }, 201

class FeedbackResource(Resource):
    def get(self, id):
        feedback = Feedback.query.get(id)
        if not feedback:
            return {"status": "error", "message": "Feedback not found"}, 404
        return {"feedback": feedback.to_dict()}, 200

api.add_resource(FeedbackListResource, "/feedbacks")
api.add_resource(FeedbackResource, "/feedbacks/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
