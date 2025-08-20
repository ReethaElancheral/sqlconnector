from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, abort
from flask_login import login_required, current_user
from models import db, Product, CartItem
from flask_wtf.csrf import CSRFProtect

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

# Provide a helper to exempt the API from CSRF (JSON only)
def csrf_exempt_bp(app):
    csrf = CSRFProtect(app)
    csrf.exempt(api_bp)
    return csrf

# ---- Resources ----
class ProductListResource(Resource):
    def get(self):
        products = Product.query.order_by(Product.created_at.desc()).all()
        data = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price_cents": p.price_cents,
                "image_url": p.image_url,
            }
            for p in products
        ]
        return jsonify(data)

class ProductResource(Resource):
    def get(self, product_id):
        p = Product.query.get_or_404(product_id)
        return jsonify({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price_cents": p.price_cents,
            "image_url": p.image_url,
        })

class CartResource(Resource):
    @login_required
    def get(self):
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        data = [
            {
                "id": i.id,
                "product_id": i.product_id,
                "name": i.product.name,
                "price_cents": i.product.price_cents,
                "quantity": i.quantity,
                "subtotal_cents": i.product.price_cents * i.quantity,
            }
            for i in items
        ]
        total_cents = sum(d["subtotal_cents"] for d in data)
        return jsonify({"items": data, "total_cents": total_cents})

class AddToCartResource(Resource):
    @login_required
    def post(self):
        payload = request.get_json(force=True) or {}
        product_id = payload.get("product_id")
        qty = int(payload.get("quantity", 1))
        if not product_id:
            abort(400, message="product_id is required")
        product = Product.query.get(product_id)
        if not product:
            abort(404, message="Product not found")
        item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if item:
            item.quantity += max(qty, 1)
        else:
            item = CartItem(user_id=current_user.id, product_id=product_id, quantity=max(qty, 1))
            db.session.add(item)
        db.session.commit()
        return jsonify({"message": "Added to cart"})

class UpdateCartItemResource(Resource):
    @login_required
    def put(self, item_id):
        payload = request.get_json(force=True) or {}
        qty = int(payload.get("quantity", 1))
        item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
        if qty <= 0:
            db.session.delete(item)
        else:
            item.quantity = qty
        db.session.commit()
        return jsonify({"message": "Cart updated"})

    @login_required
    def delete(self, item_id):
        item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed"})

api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:product_id>")
api.add_resource(CartResource, "/cart")
api.add_resource(AddToCartResource, "/cart/add")
api.add_resource(UpdateCartItemResource, "/cart/item/<int:item_id>")
