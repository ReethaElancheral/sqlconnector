from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Sample product data
products = [
    {"id": 1, "name": "Laptop", "price": 800, "in_stock": True},
    {"id": 2, "name": "Smartphone", "price": 500, "in_stock": True},
    {"id": 3, "name": "Headphones", "price": 50, "in_stock": True},
    {"id": 4, "name": "Keyboard", "price": 30, "in_stock": False},
    {"id": 5, "name": "Mouse", "price": 20, "in_stock": True}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/products", methods=["GET"])
def get_products():
    query = request.args.get("q", "").lower()
    if query:
        filtered = [p for p in products if query in p["name"].lower()]
    else:
        filtered = products
    return jsonify(filtered)

if __name__ == "__main__":
    app.run(debug=True)
