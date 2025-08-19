from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Book
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
class BookListResource(Resource):
    def get(self):
        author_filter = request.args.get("author")
        if author_filter:
            books = Book.query.filter_by(author=author_filter).all()
        else:
            books = Book.query.all()
        return {"books": [b.to_dict() for b in books]}, 200

    def post(self):
        data = request.get_json()
        if not data or "title" not in data or "author" not in data:
            return {"error": "Title and author are required"}, 400

        new_book = Book(
            title=data["title"],
            author=data["author"],
            year=data.get("year")
        )
        db.session.add(new_book)
        db.session.commit()
        return new_book.to_dict(), 201

class BookResource(Resource):
    def get(self, id):
        book = Book.query.get(id)
        if not book:
            return {"error": "Book not found"}, 404
        return book.to_dict(), 200

    def put(self, id):
        book = Book.query.get(id)
        if not book:
            return {"error": "Book not found"}, 404

        data = request.get_json()
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        if "year" in data:
            book.year = data["year"]

        db.session.commit()
        return book.to_dict(), 200

    def delete(self, id):
        book = Book.query.get(id)
        if not book:
            return {"error": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted"}, 200

# Add resources
api.add_resource(BookListResource, "/books")
api.add_resource(BookResource, "/books/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
