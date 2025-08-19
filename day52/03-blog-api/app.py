from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Post
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
class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        return {"posts": [p.to_dict() for p in posts]}, 200

    def post(self):
        data = request.get_json()
        if not data or "title" not in data or "content" not in data:
            return {"error": "Title and content are required"}, 400

        new_post = Post(
            title=data["title"],
            content=data["content"],
            author=data.get("author", "")
        )
        db.session.add(new_post)
        db.session.commit()
        return new_post.to_dict(), 201

class PostResource(Resource):
    def get(self, id):
        post = Post.query.get(id)
        if not post:
            return {"error": "Post not found"}, 404
        return post.to_dict(), 200

    def put(self, id):
        post = Post.query.get(id)
        if not post:
            return {"error": "Post not found"}, 404

        data = request.get_json()
        if "title" in data:
            post.title = data["title"]
        if "content" in data:
            post.content = data["content"]
        if "author" in data:
            post.author = data["author"]

        db.session.commit()
        return post.to_dict(), 200

    def delete(self, id):
        post = Post.query.get(id)
        if not post:
            return {"error": "Post not found"}, 404
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 200

# Add resources
api.add_resource(PostListResource, "/posts")
api.add_resource(PostResource, "/posts/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
