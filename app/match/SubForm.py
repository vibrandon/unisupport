from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField 
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class AutoMatchInputForm(FlaskForm):
    interests = TextAreaField('interests', validators=[DataRequired()])
    submit = SubmitField('Sign In')