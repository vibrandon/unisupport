from flask import render_template, redirect, url_for, flash, Blueprint, request
from markupsafe import Markup

from app.DBAccessor import DBAccessor
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
        reward_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
        flash(f'Thank you for completing this week\'s wellbeing survey!'
                 f'\nHere is your reward code!'
                 f'\n{reward_code}', 'success')

        #Database integration
        #Get question/answer dictionary pairs from returnQuestions() and total from returnTotal()

        questions = form.returnQuestions()
        mental_health_total = form.returnTotal()

        wellbeing_result = form.getWellBeingStatus()
        wellbeing_status = wellbeing_result["status"]
        wellbeing_score = wellbeing_result["score"]
        # split the wellbeing result into two parts
        # status(String) = [excellent, good ...]
        # score = float 0.0 - 10.0

        category_scores = form.calculateCategoryScores()
        recommendations = form.personalisedRecommendations()
        recommendations_csv = "|".join(recommendations)
        # csv style but with | to avoid , conflicts

        #create DB accessor object
        db_accessor = DBAccessor()
        if current_user.wellbeingProfile:
            db_accessor.update_wellbeing_profile(
                user=current_user,
                wellbeing_status=wellbeing_status,
                wellbeing_score=wellbeing_score,
                recommendations_csv=recommendations_csv
            )
        else:
            # Create new profile
            db_accessor.new_wellbeing_profile(
                    user=current_user,
                    wellbeing_status=wellbeing_status,
                    wellbeing_score=wellbeing_score,
                    recommendations_csv=recommendations_csv
            )
            """
            If total above certain value, or certain worrying responses detected,
            change WellbeingProfile's wellbeingStatus to more negative result. 
            """

        db_accessor.record_student_survey(current_user)
        return redirect(url_for('home'))

    return render_template('generic_form.html', title="Student Wellbeing Survey", form=form)

# deleted professional survey


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


# /survey/wellbeing
@survey_bp.route('/wellbeing')
@login_required
def wellbeing_profile():
    if current_user.type != 'student':
        flash("Only students can access this page.", "warning")
        return redirect(url_for('home'))

    wellbeing_profile = current_user.wellbeingProfile

    if not wellbeing_profile:
        flash("Please complete a wellbeing survey to view your profile.", "info")
        return redirect(url_for('survey.student_survey'))

    status = wellbeing_profile.wellbeingStatus
    score = wellbeing_profile.wellbeingScore
    recommendations = []
    recommendations = wellbeing_profile.recommendations.split("|")

    return render_template('wellbeing_profile.html', title='Wellbeing profile', wellbeing_profile=wellbeing_profile, score=score, status=status, recommendations=recommendations)
