from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0)])
    in_stock = BooleanField("In Stock")
    description = TextAreaField("Description")
    submit = SubmitField("Save")
