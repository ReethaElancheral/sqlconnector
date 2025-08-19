from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Task
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
class TaskList(Resource):
    def get(self):
        tasks = Task.query.all()
        return {"tasks": [t.to_dict() for t in tasks]}, 200

    def post(self):
        data = request.get_json()
        if not data or "title" not in data:
            return {"error": "Task title is required"}, 400

        new_task = Task(title=data["title"])
        db.session.add(new_task)
        db.session.commit()
        return new_task.to_dict(), 201

class TaskResource(Resource):
    def get(self, id):
        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404
        return task.to_dict(), 200

    def put(self, id):
        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404

        data = request.get_json()
        if "title" in data:
            task.title = data["title"]
        if "status" in data:
            task.status = bool(data["status"])  # toggle status
        db.session.commit()
        return task.to_dict(), 200

    def delete(self, id):
        task = Task.query.get(id)
        if not task:
            return {"error": "Task not found"}, 404
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}, 200

# Add resources
api.add_resource(TaskList, "/tasks")
api.add_resource(TaskResource, "/tasks/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
