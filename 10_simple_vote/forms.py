from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class VoteForm(FlaskForm):
    voter_name = StringField("Your Name", validators=[DataRequired()])
    candidate_id = SelectField("Candidate", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Vote")

class CandidateForm(FlaskForm):
    name = StringField("Candidate Name", validators=[DataRequired()])
    party = StringField("Party", validators=[DataRequired()])
    submit = SubmitField("Add Candidate")
