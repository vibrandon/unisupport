from flask_login import current_user
from flask_wtf import FlaskForm
from markupsafe import escape, Markup
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
    confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message="Passwords must templates")])
    submit = SubmitField('Change Password')

    def validate_password(form, field):
        if not current_user.check_password(form.password.data):
            raise ValidationError("Incorrect password")

class ChatbotForm (FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

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
                          choices=[(10, '1 - Very Low'), (9, '2'), (8, '3'), (7, '4'),
                                   (6, '5 - Moderate'), (5, '6'), (4, '7'), (3, '8'), (2, '9'),
                                   (1, '10 - Very High')], validators=[DataRequired()])

    stress_2 = SelectField("Have you been able to find enjoyment recently during your downtime or extracurriculars?",
                           choices=[(1, "Haven't participated in extracurriculars that i enjoy recently"),
                                    (2, "Not found enjoyment"),
                                    (3, "Participated or enjoyed less than I hoped"),
                                    (4, "I have found some enjoyment in my downtime"),
                                    (5, "I have participated and enjoyed extracurriculars and downtime as normal")], validators=[DataRequired()])

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
                            choices=[(6, 'Easy'),
                                     (5, 'Reasonable'),
                                     (4, 'Manageable'),
                                     (3, 'Reasonably challenging'),
                                     (2, 'Stressful'),
                                     (1, 'Overwhelming')], validators=[DataRequired()])

    academic_2 = SelectField("How do you feel you are keeping up with the demands of your course?",
                             choices=[(4, 'I am up to date and comfortable with my course'),
                                      (3, 'I am keeping up'),
                                      (2, 'I am slightly behind'),
                                      (1, 'I am significantly behind')], validators=[DataRequired()])

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

    def returnTotal(self):
        mental_health_total = int(self.stress_1.data)
        mental_health_total += int(self.stress_2.data)
        mental_health_total += int(self.sleep_1.data)
        mental_health_total += int(self.physical_1.data)
        mental_health_total += int(self.social_1.data)
        mental_health_total += int(self.academic_1.data)
        mental_health_total += int(self.academic_2.data)
        mental_health_total += int(self.engagement_1.data)
        return mental_health_total

    def getWellBeingStatus(self):
        total = self.returnTotal()
        # total possible score = 44 = perfect wellbeing score
        score = round((total/44)*10, 1)
        if score >= 8:
            status = "Excellent"
        elif score >= 6:
            status = "Good"
        elif score >= 4:
            status = "Fair"
        else:
            status = "Needs attention"
        return {
            "status": status,
            "score": score
        }

    def calculateCategoryScores(self):
        # Calculating average score 0-10 for each category
        stress_total = int(self.stress_1.data) + int(self.stress_2.data)
        stress_score = (stress_total / 15) * 10
        # stress has 15 total points - same logic for the rest of the categories
        sleep_total = int(self.sleep_1.data)
        sleep_score = (sleep_total / 5) * 10

        physical_total = int(self.physical_1.data)
        physical_score = (physical_total / 5) * 10

        social_total = int(self.social_1.data)
        social_score = (social_total / 4) * 10

        academic_total = int(self.academic_1.data) + int(self.academic_2.data)
        academic_score = (academic_total / 10) * 10

        engagement_total = int(self.engagement_1.data)
        engagement_score = (engagement_total / 5) * 10

        category_scores = {
            "stress": round(stress_score, 1),
            "sleep": round(sleep_score, 1),
            "physical": round(physical_score, 1),
            "social": round(social_score, 1),
            "academic": round(academic_score, 1),
            "engagement": round(engagement_score, 1)
        }
        return category_scores

    def personalisedRecommendations(self):
        category_scores = self.calculateCategoryScores()
        recommendations = []

        # Thresholds x<5.0 = low, 5.0<x<7.0 = medium
        if category_scores["stress"] < 5.0:
            recommendations.append("Take time to schedule regular breaks and do the things you enjoy, you may be burnt out")
            recommendations.append("Try matching with a professional through our matching services, they may be able to help manage or identify the source of your stress.")
        elif category_scores["stress"] < 7.0:
            recommendations.append("Incorporate intentional relaxation or mindfulness into your daily routine")

        if category_scores["sleep"] < 5.0:
            recommendations.append("Prioritise your sleep quality and duration this week!")
            recommendations.append("Perhaps develop a night time routine, a time to destress and establish consistency")
        elif category_scores["sleep"] < 7.0:
            recommendations.append("Perhaps try to improve your sleeping environment. Good sleep can improve many aspects of our lives")

        if category_scores["physical"] < 5.0:
            recommendations.append("Incorporate at least 150 minutes of activity this week, start slow, and ease it into your routine.")
            recommendations.append("Perhaps join a sports club or find sports/fitness opportunities through our matching system!")
        elif category_scores["physical"] < 7.0:
            recommendations.append("You are on the right track, perhaps find a partner to sustain motivation or vary your activities!")

        if category_scores["social"] < 5.0:
            recommendations.append("Reach out to close friends and family even if brief, your social connections are always valuable")
            recommendations.append("Consider attending society events this week, some opportunities can be found on the university website or through our matching system")
        elif category_scores["social"] < 7.0:
            recommendations.append("consider partaking in more group activities this week")

        if category_scores["academic"] < 5.0:
            recommendations.append("Contact your personal tutor to discuss management or deferral options")
            recommendations.append("It is normal to fall behind sometimes, forming a study group or studying with friends may help you stay on top of work")
        elif category_scores["academic"] < 7.0:
            recommendations.append("Consider changing your approach to studying, reaching out to a tutor or academic advisor may help")

        if category_scores["engagement"] < 5.0:
            recommendations.append("Please access our matching system to find a counselor to assist with planning for the future")
            recommendations.append("Focus on your daily accomplishments and remember to reward yourself")
        elif category_scores["engagement"] < 7.0:
            recommendations.append("Consider wellbeing techniques such as journaling to practice reflection in positive ways")

        if not recommendations: # perfect mental health score with no recommendations
            recommendations = ["You are doing great, keep it up and keep monitoring your wellbeing through these services"]

        return recommendations

    def returnQuestions(self):
        qList = ("How would you rate your stress level's this week?\n"
            "Have you been able to find enjoyment recently during your downtime or extracurriculars?\n"
            "How would you rate your overall sleep quality this week?\n"
            "How many days this week have you engaged in exercise for 30 minutes or more?\n"
            "How would you describe your social connectivity over the last week?\n"
            "How challenging has the last week been academically?\n"
            "How do you feel you are keeping up with the demands of your course?\n"
            "How are you feeling about the near future?\n"
            "Have you recently, or do you plan to access support via our matching services?\n")


        return qList
