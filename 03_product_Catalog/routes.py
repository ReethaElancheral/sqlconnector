from flask import render_template, request, redirect, url_for, flash, jsonify
from models import db, Product

def register_routes(app):

    @app.route('/')
    def index():
        products = Product.query.all()
        in_stock = Product.query.filter_by(in_stock=True).all()
        return render_template('index.html', products=products, in_stock=in_stock)

    @app.route('/create', methods=['GET','POST'])
    def create():
        if request.method == 'POST':
            product = Product(
                name=request.form['name'],
                price=float(request.form['price']),
                in_stock=('in_stock' in request.form),
                description=request.form['description']
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('create.html')

    @app.route('/edit/<int:id>', methods=['GET','POST'])
    def edit(id):
        product = Product.query.get_or_404(id)
        if request.method == 'POST':
            product.name = request.form['name']
            product.price = float(request.form['price'])
            product.in_stock = ('in_stock' in request.form)
            product.description = request.form['description']
            db.session.commit()
            flash('Product updated successfully!', 'info')
            return redirect(url_for('index'))
        return render_template('edit.html', product=product)

    @app.route('/delete/<int:id>')
    def delete(id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'danger')
        return redirect(url_for('index'))

    # API routes for Postman
    @app.route('/api/products', methods=['GET'])
    def api_get_products():
        products = Product.query.all()
        return jsonify([{
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "in_stock": p.in_stock,
            "description": p.description
        } for p in products])

    @app.route('/api/products/<int:id>', methods=['GET'])
    def api_get_product(id):
        p = Product.query.get_or_404(id)
        return jsonify({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "in_stock": p.in_stock,
            "description": p.description
        })

    @app.route('/api/products', methods=['POST'])
    def api_create_product():
        data = request.json
        p = Product(
            name=data['name'],
            price=data['price'],
            in_stock=data.get('in_stock', True),
            description=data.get('description','')
        )
        db.session.add(p)
        db.session.commit()
        return jsonify({"message":"Product created"}),201

    @app.route('/api/products/<int:id>', methods=['PUT'])
    def api_update_product(id):
        p = Product.query.get_or_404(id)
        data = request.json
        p.name = data.get('name', p.name)
        p.price = data.get('price', p.price)
        p.in_stock = data.get('in_stock', p.in_stock)
        p.description = data.get('description', p.description)
        db.session.commit()
        return jsonify({"message":"Product updated"})

    @app.route('/api/products/<int:id>', methods=['DELETE'])
    def api_delete_product(id):
        p = Product.query.get_or_404(id)
        db.session.delete(p)
        db.session.commit()
        return jsonify({"message":"Product deleted"})
