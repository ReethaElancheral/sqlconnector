from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description")
    price = FloatField("Price", validators=[DataRequired()])
    submit = SubmitField("Submit")
