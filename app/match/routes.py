from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory, Blueprint
from app.models import Professional 
from app.match.SubForm import ChooseForm,AutoMatchInputForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app.DBAccessor import DBAccessor
from app import db
from flask import g

match_bp = Blueprint("match_bp", __name__, template_folder="templates")

# =====================
#  Match
# =====================

@match_bp.route("/auto",methods=['post'])
@login_required
def autoMatch():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    # Example student profile (can come from a form or current_user preferences)
    autoMatchInputForm = AutoMatchInputForm()
    if not autoMatchInputForm.validate_on_submit():
        flash("Please input your interests", "danger")
        return render_template('match.html', title="Match",autoMatchInputForm=autoMatchInputForm)
    student_interests= autoMatchInputForm.interests.data
    # Load all professionals
    professionals = db.session.scalars(db.select(Professional)).all()

    # Create a list of professional descriptions
    prof_profiles = [f"{p.specialty}" for p in professionals]

    # Combine student and professional data for vectorizing
    profiles = [student_interests] + prof_profiles

    # Convert to vectors using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(profiles)

    # Calculate cosine similarity between student and each professional
    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]  # shape (n_profs,)

    # Attach similarity scores
    scored_profs = list(zip(professionals, similarities))

    # Sort by similarity
    scored_profs.sort(key=lambda x: x[1], reverse=True)

    chooseForm = ChooseForm()
    return render_template("/auto_candidates.html", title="Matched Professionals", scored_profs=scored_profs,chooseForm=chooseForm)

@match_bp.route("/")
@login_required
def match():
    autoMatchInputForm = AutoMatchInputForm()
    return render_template('match.html', title="Match",autoMatchInputForm=autoMatchInputForm)

@match_bp.route("/manual")
@login_required
def manualMatch():
    from app.models import Professional  # if not already imported
    professionals = db.session.scalars(db.select(Professional)).all()
    chooseForm = ChooseForm()
    return render_template("manual_candidates.html", title="Professionals", professionals=professionals,chooseForm=chooseForm)

@match_bp.route("/matchProf", methods=['POST'])
@login_required
def matchProf():
    form = ChooseForm()
    sid = current_user.get_id()
    if form.validate_on_submit():
        selected_id = int(form.choice.data)
        professional = db.session.get(Professional, selected_id)
        dbAccessor = DBAccessor()
        dbAccessor.match_professional(sid,selected_id)
        if professional:
            return render_template(
                'notification.html',
                title="Matching Notification",
                professionals=professional  # even if it's a single one, Jinja will access it
            )
    flash("Invalid selection", "danger")
    return render_template('/match/notification.html', title="Matching Notification",prof=professional)
    # return redirect(url_for('match_bp.manualMatch'))