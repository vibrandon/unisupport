from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, PasswordField, BooleanField
from wtforms.fields.choices import SelectField, RadioField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional
from app import db
from app.models import User

class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


def password_policy(form, field):
    message = """A password must be at least 8 characters long, and have an
                uppercase and lowercase letter, a digit, and a character which is
                neither a letter or a digit"""
    if len(field.data) < 8:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = flg_non_let_dig = False
    for ch in field.data:
        flg_upper = flg_upper or ch.isupper()
        flg_lower = flg_lower or ch.islower()
        flg_digit = flg_digit or ch.isdigit()
        flg_non_let_dig = flg_non_let_dig or not ch.isalnum()
    if not (flg_upper and flg_lower and flg_digit and flg_non_let_dig):
        raise ValidationError(message)

class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), password_policy])
    confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message="Passwords must match")])
    submit = SubmitField('Change Password')

    def validate_password(form, field):
        if not current_user.check_password(form.password.data):
            raise ValidationError("Incorrect password")


class RegisterForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_policy])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    userType = SelectField("Register as", choices=[('student', 'Student'), ('professional', 'Professional')])
    submit = SubmitField('Register')

    def validate_username(form, field):
        q = db.select(User).where(User.username==field.data)
        if db.session.scalar(q):
            raise ValidationError("Username already taken, please choose another")

    def validate_email(form, field):
        q = db.select(User).where(User.email==field.data)
        if db.session.scalar(q):
            raise ValidationError("Email address already taken, please choose another")

class UpdateAccountForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

class StudentUpdateForm(FlaskForm):
    degree = StringField("Degree", validators=[Optional()])
    address = StringField("Address", validators=[Optional()])
    submit = SubmitField("Update Student Info")

class ProfessionalUpdateForm(FlaskForm):
    workplace = StringField("Workplace", validators=[Optional()])
    specialty = StringField("Specialty", validators=[Optional()])
    submit = SubmitField("Update Professional Info")


class NotRealSurvey(FlaskForm):  # placeholder
    question_1 = SelectField("question_1", choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[DataRequired()])
    question_2 = RadioField("question_1", choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[DataRequired()])
    question_3 = SelectField("question_1", choices=[('1', '1'), ('2', '2'), ('3', '3')], validators=[DataRequired()])
    submit = SubmitField("Submit")

class StudentSurveyForm(FlaskForm):  # questions subject to change
    stress_1 = SelectField("How would you rate your stress level's this week?",
                          choices=[(1, '1 - Very Low'), (2, '2'), (3, '3'), (4, '4'),
                                   (5, '5 - Moderate'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),
                                   (10, '10 - Very High')], validators=[DataRequired()])

    stress_2 = SelectField("Have you been able to find enjoyment recently during your downtime or extracurriculars?",
                           choices=[(1, "Haven't participated in extracurriculars that i enjoy recently"), (2, "Not found enjoyment"), (3, "Participated or enjoyed less than I hoped"), (4, "I have found some enjoyment in my downtime"), (5, "I have participated and enjoyed extracurriculars and downtime as normal")], validators=[DataRequired()])

    sleep_1 = SelectField("How would you rate your overall sleep quality this week?",
                         choices=[(1, 'Very poor: I have consistently been feeling fatigued and unable to complete daily activities well, with detriment to my physical wellbeing or sleeping behaviour'),
                                  (2, 'Poor: I am often feeling fatigued or drowsy, occasionally affecting my ability to perform daily tasks.'),
                                  (3, 'Okay: I have neither felt low or high energy throughout the week.'),
                                  (4, 'Good: I have had good quality sleep, and have performed well this week'),
                                  (5, 'Excellent: I have consistently had good quality sleep throughout the week, and I have been feeling great')], validators=[DataRequired()])

    physical_1 = RadioField("How many days this week have you engaged in exercise for 30 minutes or more?",
                            choices=[(1, '0 days'),
                                     (2, '1-2 days'),
                                     (3, '3-4 days'),
                                     (4, '5-6 days'),
                                     (5, 'Every day')], validators=[DataRequired()])

    social_1 = SelectField("How would you describe your social connectivity over the last week?",
                           choices=[(1, "I have felt isolated and lonely recently"),
                                    (2, "I spent the majority of my time alone this week"),
                                    (3, "I spent some time with others this week"),
                                    (4, "I spent quality time with those close to me frequently")], validators=[DataRequired()])

    academic_1 = RadioField("How challenging has the last week been academically?",
                            choices=[(1, 'Easy'),
                                     (2, 'Reasonable'),
                                     (3, 'Manageable'),
                                     (4, 'Reasonably challenging'),
                                     (5, 'Stressful'),
                                     (6, 'Overwhelming')], validators=[DataRequired()])

    academic_2 = SelectField("How do you feel you are keeping up with the demands of your course?",
                             choices=[(1, 'I am up to date and comfortable with my course'),
                                      (2, 'I am keeping up'),
                                      (3, 'I am slightly behind'),
                                      (4, 'I am significantly behind')], validators=[DataRequired()])

    engagement_1 = RadioField("How are you feeling about the near future?",
                               choices=[(1, "Anxiety"),
                                        (2, "Out of your control"),
                                        (3, "Indifferent"),
                                        (4, "Hopeful"),
                                        (5, "Positive")], validators=[DataRequired()])

    engagement_2 = RadioField("Have you recently, or do you plan to access support via our matching services?",
                              choices=[(1, "No"),
                                       (2, "Yes")], validators=[DataRequired()])
    submit = SubmitField("Submit to claim your store token")
