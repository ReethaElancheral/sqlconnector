from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from wtforms.validators import Email

main = Blueprint('main', __name__)

class Student(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    roll_no = db.Column(String(20), unique=True, nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    age = db.Column(Integer, nullable=False)

# HTML Routes
@main.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@main.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        age = request.form['age']

        # Email validation
        if '@' not in email:
            flash('Invalid email address', 'danger')
            return redirect(url_for('main.add_student'))

        student = Student(name=name, roll_no=roll_no, email=email, age=age)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_student.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll_no = request.form['roll_no']
        student.email = request.form['email']
        student.age = request.form['age']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_student.html', student=student)

@main.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('main.index'))

# POSTMAN API Routes
@main.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        "id": s.id,
        "name": s.name,
        "roll_no": s.roll_no,
        "email": s.email,
        "age": s.age
    } for s in students])

@main.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(**data)
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student created"}), 201

@main.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify({"message": "Student updated"})

@main.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student_api(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"})
