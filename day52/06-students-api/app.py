from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Student
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)

VALID_GRADES = {"A", "B", "C", "D"}

class StudentListResource(Resource):
    def get(self):
        students = Student.query.all()
        return {"students": [s.to_dict() for s in students]}, 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "roll" not in data or "grade" not in data:
            return {"status": "error", "message": "name, roll, and grade are required"}, 400

        if data["grade"] not in VALID_GRADES:
            return {"status": "error", "message": "Grade must be A, B, C, or D"}, 400

        new_student = Student(name=data["name"], roll=data["roll"], grade=data["grade"])
        db.session.add(new_student)
        db.session.commit()
        return {"status": "success", "student": new_student.to_dict()}, 201

class StudentResource(Resource):
    def get(self, id):
        student = Student.query.get(id)
        if not student:
            return {"status": "error", "message": "Student not found"}, 404
        return {"status": "success", "student": student.to_dict()}, 200

    def put(self, id):
        student = Student.query.get(id)
        if not student:
            return {"status": "error", "message": "Student not found"}, 404

        data = request.get_json()
        if "name" in data:
            student.name = data["name"]
        if "roll" in data:
            student.roll = data["roll"]
        if "grade" in data:
            if data["grade"] not in VALID_GRADES:
                return {"status": "error", "message": "Grade must be A, B, C, or D"}, 400
            student.grade = data["grade"]

        db.session.commit()
        return {"status": "success", "student": student.to_dict()}, 200

    def delete(self, id):
        student = Student.query.get(id)
        if not student:
            return {"status": "error", "message": "Student not found"}, 404
        db.session.delete(student)
        db.session.commit()
        return {"status": "success", "message": "Student deleted"}, 200

# Routes
api.add_resource(StudentListResource, "/students")
api.add_resource(StudentResource, "/students/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
