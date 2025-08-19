from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

api = Api(app)

# Resources
class UserList(Resource):
    def get(self):
        users = User.query.all()
        return {"users": [u.to_dict() for u in users]}, 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "email" not in data:
            return {"error": "Name and email required"}, 400

        if User.query.filter_by(email=data["email"]).first():
            return {"error": "Email already exists"}, 400

        new_user = User(name=data["name"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    def put(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        data = request.get_json()
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        db.session.commit()
        return user.to_dict(), 200

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {"error": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

# Add resources
api.add_resource(UserList, "/users")
api.add_resource(UserResource, "/users/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
