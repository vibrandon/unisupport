from flask import Flask
from config import Config
from jinja2 import StrictUndefined
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy as sa
import sqlalchemy.orm as so


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'



from app import views, models
from app.debug_utils import reset_db


from app.chat.userMessaging import user_msg_bp
app.register_blueprint(user_msg_bp,url_prefix="/userMessaging")

from app.chat.chatbot.routes import chatbot_bp
app.register_blueprint(chatbot_bp,url_prefix="/chatbot")

from app.chat.routes import chat_bp
app.register_blueprint(chat_bp,url_prefix="/chat")

from app.auth.routes import auth_bp
app.register_blueprint(auth_bp,url_prefix="/auth")

from app.admin import admin_bp
app.register_blueprint(admin_bp,url_prefix="/admin")

from app.match.routes import match_bp
app.register_blueprint(match_bp,url_prefix="/match")

from app.survey import survey_bp
app.register_blueprint(survey_bp, url_prefix="/survey")

from app.account.routes import account_bp
app.register_blueprint(account_bp, url_prefix="/account")





@app.shell_context_processor
def make_shell_context():
    return dict(db=db, sa=sa, so=so, reset_db=reset_db)
