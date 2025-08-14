from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Task
from datetime import datetime

main = Blueprint("main", __name__)

@main.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template("index.html", tasks=tasks)

@main.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        due_date = request.form['due_date']
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
        task = Task(title=title, due_date=due_date_obj)
        db.session.add(task)
        db.session.commit()
        flash("Task added!", "success")
        return redirect(url_for('main.index'))
    return render_template("add_task.html")

@main.route('/toggle/<int:id>')
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "danger")
    return redirect(url_for('main.index'))
