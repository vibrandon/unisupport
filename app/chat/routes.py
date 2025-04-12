from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models import Professional, Student

chat_bp = Blueprint("chat_bp", __name__, url_prefix="/chat/messages",template_folder="templates")


@chat_bp.route("/")
@login_required
def chat():
    if current_user.type == 'student':
        users = db.session.scalars(db.select(Professional)).all()
    elif current_user.type == 'professional':
        users = db.session.scalars(db.select(Student)).all()
    else:
        users = []

    return render_template('chat.html', title="Chat", users=users)