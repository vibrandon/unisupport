from flask import render_template, redirect, url_for, flash, Blueprint, request
from markupsafe import Markup
from app.models import studentSurvey, professionalSurvey, wellbeingProfile
from app.forms import NotRealSurvey, StudentSurveyForm
from flask_login import current_user,login_required
import sqlalchemy as sa
from app import db, app
# NEW IMPORTS
import random
from datetime import datetime, timedelta, date

survey_bp = Blueprint("survey_bp", __name__, template_folder="templates")


# Survey Route  # RANDOM IMPORTED
@survey_bp.route('/student_survey', methods=['GET', 'POST'])
@login_required
def student_survey():
    if current_user.type != 'student':
        flash("students only.", "danger")
        return redirect(url_for('home'))

    form = StudentSurveyForm()


    if form.validate_on_submit():
        # Reward token, Incentive for the Student to complete the survey
        reward_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        flash(f'Thank you for completing this week\'s wellbeing survey!'
                 f'\nHere is your reward code!'
                 f'\n{reward_code}', 'success')

        #Database integration
        #Get question/answer dictionary pairs from returnQuestions() and total from returnTotal()

        questions = form.returnQuestions()
        mental_health_total = form.returnTotal()

        """
        If total above certain value, or certain worrying responses detected,
        change WellbeingProfile's wellbeingStatus to more negative result. 
        """
        if mental_health_total > 10:
            #update wellbeing profile to display that this result is worrying.
            #look for wellbeing profile:
            if current_user.wellbeingProfile:
                current_user.wellbeingProfile.wellbeingStatus = "Worrying"
                current_user.wellbeingProfile.recommendations += ["Improve Sleep","Improve excercise",
                                                                   "Match with professional"]
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
            #if it is not there, create wellbeing profile
            else:
                new_well_profile = wellbeingProfile(
                    student=current_user,
                    studentID=current_user.id,
                    wellbeingStatus="Worrying",
                    recommendations=["Improve Sleep",
                                     "Improve excercise",
                                     "Match with professional"]
                )
                try:
                    db.session.add(new_well_profile)
                    db.session.commit()
                except:
                    db.session.rollback()

        try:
            survey = studentSurvey(
                id=current_user.id,
                student=current_user,
                studentID=current_user.id,
                timestamp=datetime.now(),
                questions=questions
            )
            db.session.add(survey)
            db.session.commit()
        except sa.exc.SQLAlchemyError as e:
            db.session.rollback()
            flash(f"{e} occurred","danger")
        return redirect(url_for('home'))

    return render_template('generic_form.html', title="Student Wellbeing Survey", form=form)


@survey_bp.route('/professional_survey', methods=['GET', 'POST'])
@login_required
def professional_survey():
    if current_user.type != 'professional':
        flash("Professionals only.", "danger")
        return redirect(url_for('home'))

    form = NotRealSurvey()
    if form.validate_on_submit():
        # Reward token
        reward_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        flash(f'Thank you for completing this week\'s wellbeing survey!'
                 f'\nHere is your reward code!'
                 f'\n{reward_code}', 'success')
        # placeholder database integration
        try:
            survey = professionalSurvey(
                professional=current_user,
                professional_id=current_user.id,
                timestamp=datetime.now(),
                questions="placeholder for professional survey questions"
            )
            #change questions from a list into a dictionary with {question:answer,question:answer} pairs
            db.session.add(survey)
            db.session.commit()
        except sa.exc.SQLAlchemyError as e:
            db.session.rollback()
            flash(f"{e} occurred","danger")

        return redirect(url_for('home'))

    return render_template('generic_form.html', title="Student-Professional Survey", form=form)


# This function handles a flash message to notify the user every sunday, when the weekly survey is released
# Else reminds the user to complete the survey throughout the week on every page.
# Note - the above reminder will always be present until db integration added to the student_survey() route
def popup_survey():
    if not current_user.is_authenticated or current_user.type != 'student':
        return  # exit function if 'student' not logged in
    # check if today is sunday

    if request.endpoint in ['static', 'login', 'survey/student_survey']:
        return  # prevents popup appearing during static requests, login, or when student is completing survey

    # Note new import
    date_today = date.today()

    days_since_sunday = date_today.weekday() + 1
    current_week_start_date = date_today - timedelta(days=days_since_sunday)

    # Has the student completed the survey, on or after the start of the current week's sunday
    q = sa.select(studentSurvey).where(studentSurvey.studentID == current_user.id).where(sa.func.date(studentSurvey.timestamp) >= current_week_start_date)
    weekly_survey_complete = db.session.scalar(q)

    if weekly_survey_complete is None:
        sunday = date_today.weekday() == 6

        #added markup to fill in placeholder for link. Also changed {{ message }} to {{ message | safe }} in "base.html" to allow this to work
        if sunday:
            message = (Markup("Your weekly wellbeing survey is now available!\n"
                             f'Complete it Here: <a href="/survey/student_survey" class="alert-link">Click Here</a> for a code for a free food/drink item'))
        else:
            # message = ("Don't forget to complete your weekly wellbeing survey!"
            #            f" Complete it Here:({url_for('student_survey')}) to claim your free food/drink item")
            message = Markup("Don't forget to complete your weekly wellbeing survey!\n"
                             f'Complete it Here: <a href="/survey/student_survey" class="alert-link">Click Here</a> for a code for a free food/drink item')

        flash(f"{message}", "primary")

@app.before_request  # note this popup appears on every page for now (10/04/2025)
def check_survey_popup():
    popup_survey()
# note 2: this popup has a minor bug where it still appears when student logs out, but refreshing removes the popup
