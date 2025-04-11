from flask import render_template, redirect, url_for, flash, request
from markupsafe import Markup

from app import app
from app.models import studentSurvey
from app.forms import NotRealSurvey
from app.models import User, Professional, Student
from app.forms import ChooseForm, LoginForm, ChangePasswordForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
# NEW IMPORTS
import random
from datetime import date, timedelta

# =====================
# 🏠 Home Route
# =====================
@app.route("/")
def home():
    return render_template('home.html', title="UniSupport")

# =====================
# ❗ Error Handlers
# =====================
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
