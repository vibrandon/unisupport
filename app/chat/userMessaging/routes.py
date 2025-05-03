from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Message, StudentChatMessage
from app.db_accessor import DBAccessor

user_messaging_bp = Blueprint("user_messaging_bp", __name__, url_prefix="/chat/messages",template_folder="templates")

db = DBAccessor()  # using DB accessor helper (wraps db calls)

@user_messaging_bp.route("/<int:user_id>", methods=["GET", "POST"])
@login_required
def chat_with_user(user_id):
    # Fetch the chat partner (target user)
    partner = db.get_user_by_id(user_id)
    if not partner:
        flash("User not found", "warning")
        return redirect(url_for('chat_bp.chat'))  # fallback if invalid user

    # Pull all messages between current user and partner (both directions)
    message = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == partner.id)) |
        ((Message.sender_id == partner.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()

    # Render chatroom template with loaded messages
    return render_template("chatroom.html", title="Chat", messages=message, chat_partner=partner)

@user_messaging_bp.route("/send_message", methods=["POST"])
@login_required
def send_message():
    # Grab message content + receiver from form POST
    content = request.form.get("content")
    rid = request.form.get("receiver_id")

    # Simple guard: skip if missing
    if not content or not rid:
        return redirect(request.referrer or url_for('chat_bp.chat'))

    # Create + store message in DB
    msg = Message(sender_id=current_user.id, receiver_id=int(rid), content=content)
    db.add_message(msg)

    # Redirect back to chat view
    return redirect(url_for("user_messaging_bp.chat_with_user", user_id=rid))


@user_messaging_bp.route("/student_room", methods=["GET", "POST"])
@login_required
def student_chat_room():
    # Only allow students
    if current_user.type != 'student':
        flash("Access denied: Only students can join the student chat room.", "warning")
        return redirect(url_for('chat_bp.chat'))

    if request.method == "POST":
        content = request.form.get("content")
        if content:
            new_msg = StudentChatMessage(sender_id=current_user.id, content=content)
            db.add_student_message(new_msg)
        return redirect(url_for('user_messaging_bp.student_chat_room'))

    # Get recent messages for display
    messages = db.get_recent_student_messages(limit=50)

    return render_template("student_chatroom.html", title="Student Chat Room", messages=messages, current_user=current_user)