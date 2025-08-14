from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^\+?\d{7,15}$', message="Enter a valid phone number")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[Length(max=200)])
    submit = SubmitField('Submit')
