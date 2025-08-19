from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False)  # False = incomplete, True = complete

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status}
