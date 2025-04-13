from flask import Blueprint, render_template, flash, session, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.chat.chatbot.chatbotfile import ChatbotMessager
from app.models import Chatbot
from app.forms import ChatbotForm

chatbot_bp = Blueprint(
    "chatbot_bp",
    __name__,
    url_prefix="/chat/chatbot",
    template_folder="templates"
)
ai_chatbot = ChatbotMessager()


@chatbot_bp.route("/ai", methods=["GET"])
@login_required
def chatbot():
    return redirect(url_for('chatbot_bp.message'))


@chatbot_bp.route("/message", methods=['GET', 'POST'])
@login_required
def message():
    form = ChatbotForm()
    if form.validate_on_submit():
        user_message = form.message.data
        user_msg = Chatbot(user_id=current_user.id, message=user_message, ChatbotMessage=False)
        db.session.add(user_msg)
        db.session.commit()
        chat_history = session.get('chat_history', [])
        chatbot_response, updated_chat_history = ai_chatbot.get_response(user_message, chat_history)
        session['chat_history'] = updated_chat_history
        chatbot_msg = Chatbot(user_id=current_user.id, message=chatbot_response, ChatbotMessage=True)
        db.session.add(chatbot_msg)
        db.session.commit()
        return redirect(url_for('chatbot_bp.message'))
    chat_history = db.session.scalars(
        db.select(Chatbot).where(Chatbot.user_id == current_user.id).order_by(Chatbot.TimeOfMessage)
    ).all()

    messages = []
    for message in chat_history:
        messages.append({
            'message': message.message,
            'ChatbotMessage': message.ChatbotMessage,
            'TimeOfMessage': message.TimeOfMessage.strftime('%H:%M:%S')
        })
    return render_template('chat.html', title="AI Chatbot", form=form, messages=messages)  # Fixed: changed 'chatbot.html' to 'chat.html'


@chatbot_bp.route("/message/reset", methods=['GET', 'POST'])
@login_required
def reset():
    session.pop('chat_history', None)
    db.session.execute(db.delete(Chatbot).where(Chatbot.user_id == current_user.id))
    db.session.commit()
    flash('Chat history cleared successfully!', 'success')
    return redirect(url_for('chatbot_bp.message'))