from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app.match import bp
from app.models import User, Professional, Student
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, RegisterForm, UpdateAccountForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db


# =====================
#  Match
# =====================
@bp.route("/auto")
@login_required
def autoMatch():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    # Example student profile (can come from a form or current_user preferences)
    student_profile = "stress anxiety academic support motivation"

    # Load all professionals
    professionals = db.session.scalars(db.select(Professional)).all()

    # Create a list of professional descriptions
    prof_profiles = [f"{p.specialty}" for p in professionals]

    # Combine student and professional data for vectorizing
    profiles = [student_profile] + prof_profiles

    # Convert to vectors using TF-IDF
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(profiles)

    # Calculate cosine similarity between student and each professional
    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]  # shape (n_profs,)

    # Attach similarity scores
    scored_profs = list(zip(professionals, similarities))

    # Sort by similarity
    scored_profs.sort(key=lambda x: x[1], reverse=True)

    return render_template("/match/auto_candidates.html", title="Matched Professionals", scored_profs=scored_profs)
@bp.route("")
@login_required
def match():
    return render_template('match/match.html', title="Match")

@bp.route("/manual")
@login_required
def manualMatch():
    from app.models import Professional  # if not already imported
    professionals = db.session.scalars(db.select(Professional)).all()
    chooseForm = ChooseForm()
    return render_template("/match/manual_candidates.html", title="Professionals", professionals=professionals,chooseForm=chooseForm)
@bp.route("/matchProf",methods=['POST'])
def matchProf():
   form = ChooseForm()
   print(form.choice)
   return render_template('/match/notification.html', title="Matching Notification")
