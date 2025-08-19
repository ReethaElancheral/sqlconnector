from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ReviewForm(FlaskForm):
    movie_title = StringField("Movie Title", validators=[DataRequired(), Length(max=200)])
    rating = IntegerField("Rating (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("Comment", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("Submit Review")
