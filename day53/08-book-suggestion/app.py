from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Sample book suggestions
books = [
    {"title": "The Alchemist", "author": "Paulo Coelho", "year": 1988},
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "year": 1937}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/book/suggest", methods=["GET"])
def suggest_book():
    book = random.choice(books)
    return jsonify(book)

if __name__ == "__main__":
    app.run(debug=True)
