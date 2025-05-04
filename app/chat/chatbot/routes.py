from flask import Blueprint, render_template, flash, session, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.db_accessor import DBAccessor
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
db_accessor = DBAccessor()


@chatbot_bp.route("/message", methods=['GET', 'POST'])
@login_required
def message():
    form = ChatbotForm()
    if form.validate_on_submit():
        user_message = form.message.data
        user_msg = Chatbot(user_id=current_user.id, message=user_message, ChatbotMessage=False)

        # Use db directly since DBAccessor doesn't have methods for chatbot
        db.session.add(user_msg)
        db.session.commit()

        chat_history = session.get('chat_history', [])
        chatbot_response, updated_chat_history = ai_chatbot.get_response(user_message, chat_history)
        session['chat_history'] = updated_chat_history

        chatbot_msg = Chatbot(user_id=current_user.id, message=chatbot_response, ChatbotMessage=True)
        db.session.add(chatbot_msg)
        db.session.commit()

        return redirect(url_for('chatbot_bp.message'))
#the function above differentiates between user and chatbot by ChatbotMessage=False or True for a chatbot and the chat history is visible in the session.
# Uses db as no query method in dbaccessor
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
    return render_template('chatbot.html', title="AI Chatbot", form=form, messages=messages)
#this section of code displays the chat history in the session; ordered by time sent, while the user messages the chatbot and the messages all have the time sent shown on them.

@chatbot_bp.route("/message/reset", methods=['GET', 'POST'])
@login_required
def reset():
    session.pop('chat_history', None)

    # again using db for deleting the chat history
    db.session.execute(db.delete(Chatbot).where(Chatbot.user_id == current_user.id))
    db.session.commit()

    flash('Chat history cleared successfully!', 'success')
    return redirect(url_for('chatbot_bp.message'))
#this section of code will delete the chat history from the live messaging session as well as the database and notifies the user of this.