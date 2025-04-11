from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Message

chat_bp = Blueprint('chat_bp', __name__, template_folder="templates")

@chat_bp.route("/chat/<int:user_id>", methods=["GET", "POST"])
@login_required
def chat_with_user(user_id):
    chat_partner = db.session.get(User, user_id)
    if not chat_partner:
        flash("User not found", "warning")
        return redirect(url_for('chat'))

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == chat_partner.id)) |
        ((Message.sender_id == chat_partner.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    return render_template("chatroom.html", title="Chat", messages=messages, chat_partner=chat_partner)


@chat_bp.route("/send_message", methods=["POST"])
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
        db.session.add(message)
        db.session.commit()

    return redirect(url_for("chat_bp.chat_with_user", user_id=receiver_id))
