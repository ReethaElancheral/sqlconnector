from flask import Blueprint, render_template, redirect, url_for, flash
from models import db, Product
from forms import ProductForm

main = Blueprint("main", __name__)

@main.route("/")
def index():
    products = Product.query.all()
    in_stock_products = Product.query.filter_by(in_stock=True).all()
    return render_template("index.html", products=products, in_stock_products=in_stock_products)

@main.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            in_stock=form.in_stock.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("add_product.html", form=form)

@main.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.in_stock = form.in_stock.data
        product.description = form.description.data
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("main.index"))
    return render_template("edit_product.html", form=form, product=product)

@main.route("/delete/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("main.index"))
