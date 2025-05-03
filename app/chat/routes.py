from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.DBAccessor import DBAccessor

chat_bp = Blueprint("chat_bp", __name__, url_prefix="/chat/messages", template_folder="templates")
db_accessor = DBAccessor()

@chat_bp.route("/")
@login_required
def chat():
    if current_user.type == 'student':
        users = db_accessor.get_all_professionals()
    elif current_user.type == 'professional':
        users = db_accessor.get_all_students()
    else:
        users = []

    return render_template('chat.html', title="Chat", users=users)
