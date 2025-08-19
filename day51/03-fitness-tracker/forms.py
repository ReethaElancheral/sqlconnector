from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
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

class WorkoutForm(FlaskForm):
    workout_type = SelectField("Workout Type", choices=[("Cardio","Cardio"), ("Strength","Strength"), ("Yoga","Yoga"), ("Other","Other")], validators=[DataRequired()])
    steps = IntegerField("Steps", default=0, validators=[NumberRange(min=0)])
    hours = FloatField("Hours", default=0.0, validators=[NumberRange(min=0)])
    submit = SubmitField("Log Workout")

class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password")
    confirm_new_password = PasswordField("Confirm New Password", validators=[EqualTo("new_password")])
    submit = SubmitField("Update Profile")
