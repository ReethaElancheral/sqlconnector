from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Workout
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)

# -------- Resources ----------
class WorkoutListResource(Resource):
    def get(self):
        workouts = Workout.query.all()
        return {"workouts": [w.to_dict() for w in workouts]}, 200

    def post(self):
        data = request.get_json()
        if not data or "user" not in data or "workout_type" not in data or "duration" not in data:
            return {"error": "user, workout_type, and duration are required"}, 400

        if not isinstance(data["duration"], int) or data["duration"] <= 0:
            return {"error": "duration must be a positive integer"}, 400

        workout = Workout(
            user=data["user"],
            workout_type=data["workout_type"],
            duration=data["duration"]
        )
        db.session.add(workout)
        db.session.commit()
        return {"message": "Workout added", "workout": workout.to_dict()}, 201


class WorkoutResource(Resource):
    def get(self, id):
        workout = Workout.query.get(id)
        if not workout:
            return {"error": "Workout not found"}, 404
        return {"workout": workout.to_dict()}, 200

    def put(self, id):
        workout = Workout.query.get(id)
        if not workout:
            return {"error": "Workout not found"}, 404

        data = request.get_json()
        if "user" in data:
            workout.user = data["user"]
        if "workout_type" in data:
            workout.workout_type = data["workout_type"]
        if "duration" in data:
            if not isinstance(data["duration"], int) or data["duration"] <= 0:
                return {"error": "duration must be a positive integer"}, 400
            workout.duration = data["duration"]

        db.session.commit()
        return {"message": "Workout updated", "workout": workout.to_dict()}, 200

    def delete(self, id):
        workout = Workout.query.get(id)
        if not workout:
            return {"error": "Workout not found"}, 404
        db.session.delete(workout)
        db.session.commit()
        return {"message": "Workout deleted"}, 200


class WorkoutSummaryResource(Resource):
    def get(self):
        workouts = Workout.query.all()
        total_duration = sum([w.duration for w in workouts])
        return {
            "total_workouts": len(workouts),
            "total_duration_minutes": total_duration
        }, 200


# -------- Routes ----------
api.add_resource(WorkoutListResource, "/workouts")
api.add_resource(WorkoutResource, "/workouts/<int:id>")
api.add_resource(WorkoutSummaryResource, "/summary")

if __name__ == "__main__":
    app.run(debug=True)
