from flask import Flask, request
from flask_restful import Api, Resource
from models import db, Product
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

api = Api(app)

# ------- Resources ---------
class ProductListResource(Resource):
    def get(self):
        products = Product.query.all()
        return {"products": [p.to_dict() for p in products]}, 200

    def post(self):
        data = request.get_json()
        if not data or "name" not in data or "price" not in data or "in_stock" not in data:
            return {"error": "name, price, and in_stock are required"}, 400

        try:
            price = float(data["price"])
            if price <= 0:
                return {"error": "Price must be greater than 0"}, 400
        except ValueError:
            return {"error": "Price must be a number"}, 400

        product = Product(name=data["name"], price=price, in_stock=bool(data["in_stock"]))
        db.session.add(product)
        db.session.commit()

        return {"message": "Product created", "product": product.to_dict()}, 201


class ProductResource(Resource):
    def get(self, id):
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404
        return {"product": product.to_dict()}, 200

    def put(self, id):
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404

        data = request.get_json()
        if "name" in data:
            product.name = data["name"]
        if "price" in data:
            try:
                price = float(data["price"])
                if price <= 0:
                    return {"error": "Price must be greater than 0"}, 400
                product.price = price
            except ValueError:
                return {"error": "Price must be a number"}, 400
        if "in_stock" in data:
            product.in_stock = bool(data["in_stock"])

        db.session.commit()
        return {"message": "Product updated", "product": product.to_dict()}, 200

    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            return {"error": "Product not found"}, 404
        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200


# ------- Routes ---------
api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)
