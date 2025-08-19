from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    workout_type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "workout_type": self.workout_type,
            "duration": self.duration
        }
