from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
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

class ExpenseForm(FlaskForm):
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField("Category", choices=[("Food","Food"), ("Transport","Transport"), ("Entertainment","Entertainment"), ("Other","Other")], validators=[DataRequired()])
    submit = SubmitField("Add Expense")

class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password")
    confirm_new_password = PasswordField("Confirm New Password", validators=[EqualTo("new_password")])
    submit = SubmitField("Update Profile")

class LimitForm(FlaskForm):
    monthly_limit = FloatField("Monthly Spending Limit", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Set Limit")
