
from flask import Blueprint, render_template, flash, session, request
from flask_login import login_required, current_user
from urllib3 import request

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
ai_chatbot= ChatbotMessager()

@chatbot_bp.route("/ai", methods=["GET"])
@login_required
def chatbot():
    return render_template("chatbot.html", title="AI Chatbot")


@chatbot_bp.route("/message", methods=['GET', 'POST'])
@login_required
def message():
    form = ChatbotForm()
    CurrentUserChatHistory = db.session.scalars(db.select(Chatbot).where(Chatbot.user_id == current_user.id).order_by(Chatbot.time)).all()

    messages = [{'msg' : message.msg, 'chatbot' : message.chatbot, 'time': message.time.strftime('%H:%M:%S') }
                for message in CurrentUserChatHistory]
    return render_template('chatbot.html', title= "AI Chatbot", form=form, messages=messages)

@chatbot_bp.route("/message/chatbot", methods=['POST'])
@login_required
def MessageChatbot():
    UserMessage =  request.json.get('message', '')
    if not UserMessage:
        return flash('Sorry, a message is needed', 'danger')

    chat_history = session.get('chat_history', [])

    user_message = Chatbot(user_id= current_user.id, message=UserMessage, ChatbotMessage=False)
    db.session.add(user_message)
    db.session.commit()
    chatbot_response, UpdatedChatHistory = ai_chatbot.get_response(user_message, chat_history)
    chatbot_message = Chatbot(user_id=current_user.id, message=chatbot_response, ChatbotMessage=True)
    db.session.add(chatbot_message)
    db.session.commit()


@chatbot_bp.route("/message/reset", methods=['POST'])
@login_required
def reset():
    session.pop('chat_history', None)
    db.session.execute(db.delete(Chatbot).where(Chatbot.user_id == current_user.id))
    db.session.commit()
    return flash('Chat history cleared successfully!', 'success')
