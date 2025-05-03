from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Message
from app.db_accessor import DBAccessor  # Make sure to import your accessor class

user_msg_bp = Blueprint("user_msg_bp", __name__, url_prefix="/chat/messages", template_folder="templates")
db_accessor = DBAccessor()

@user_msg_bp.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def chat_with_user(user_id):
    chat_partner = db_accessor.get_user_by_id(user_id)
    if not chat_partner:
        flash("User not found", "warning")
        return redirect(url_for('chat_bp.chat'))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == chat_partner.id)) |
        ((Message.sender_id == chat_partner.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    return render_template("chatroom.html", title="Chat", messages=messages, chat_partner=chat_partner)


@user_msg_bp.route("/send_message", methods=["POST"])
@login_required
def send_message():
    content = request.form.get("content")
    receiver_id = request.form.get("receiver_id")

    if content and receiver_id:
        message = Message(
            sender_id=current_user.id,
            receiver_id=int(receiver_id),
            content=content
        )
        db_accessor.add_message(message)

    return redirect(url_for("chat_bp.chat_with_user", user_id=receiver_id))
