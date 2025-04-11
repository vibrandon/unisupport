from flask import Blueprint, render_template
from flask_login import login_required

chatbot_bp = Blueprint(
    "chatbot_bp",
    __name__,
    url_prefix="/chat/chatbot",
    template_folder="templates"
)

@chatbot_bp.route("/ai", methods=["GET"])
@login_required
def chatbot():
    return render_template("chatbot.html", title="AI Chatbot")
