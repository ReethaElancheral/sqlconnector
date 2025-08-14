from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Book

main = Blueprint("main", __name__)

@main.route("/")
def index():
    books = Book.query.order_by(Book.published_year).all()
    return render_template("index.html", books=books)

@main.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        quantity = int(request.form['quantity'])
        published_year = int(request.form['published_year'])
        book = Book(title=title, author=author, quantity=quantity, published_year=published_year)
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template("add_book.html")

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == "POST":
        book.title = request.form['title']
        book.author = request.form['author']
        book.quantity = int(request.form['quantity'])
        book.published_year = int(request.form['published_year'])
        db.session.commit()
        flash("Book updated successfully!", "success")
        return redirect(url_for('main.index'))
    return render_template("edit_book.html", book=book)

@main.route("/delete/<int:id>")
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted!", "danger")
    return redirect(url_for('main.index'))
