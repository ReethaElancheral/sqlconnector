from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class QuizForm(FlaskForm):
    # Example 3-question quiz
    q1 = RadioField("What is 2+2?", choices=[("3","3"), ("4","4"), ("5","5")], validators=[DataRequired()])
    q2 = RadioField("Capital of France?", choices=[("Paris","Paris"), ("Rome","Rome"), ("Berlin","Berlin")], validators=[DataRequired()])
    q3 = RadioField("Python is a ...?", choices=[("Snake","Snake"), ("Language","Language"), ("Car","Car")], validators=[DataRequired()])
    submit = SubmitField("Submit Quiz")
