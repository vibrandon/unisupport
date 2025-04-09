from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
from datetime import datetime

# =========================
# 👤 User Model
# =========================

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64))
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    phoneNumber: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64), unique=True, nullable=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(64))  # will hold "student" or "professional"
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    type: so.Mapped[str] = so.mapped_column(sa.String(50))  # discriminator column

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role})'

@dataclass
class Student(User):
    __tablename__ = 'students'
    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)
    degree: so.Mapped[str] = so.mapped_column(sa.String(120),nullable=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(256),nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


@dataclass
class Professional(User):
    __tablename__ = 'professionals'
    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)
    workplace: so.Mapped[str] = so.mapped_column(sa.String(120),nullable=True)
    specialty: so.Mapped[str] = so.mapped_column(sa.String(120),nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "professional",
    }

class Admin(User):
    __tablename__ = 'admins'

@dataclass()
class Chatbot(db.Model):
    __tablename__ = 'MessagesWithChatbot'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    message: so.Mapped[str] = so.mapped_column(sa.Text)
    ChatbotMessage: so.Mapped[bool] = so.mapped_column(default=False)
    TimeOfMessage: so.Mapped[datetime] = so.mapped_column(sa.DateTime,default=sa.func.now())
    user: so.Mapped['User'] = relationship(back_populates='MessagesWithChatbot')

    def __repr__(self):
        return f'Chatbot(id={self.id}, user_id={self.user_id}, ChatbotMessage={self.ChatbotMessage})'


# @dataclass
# class wellbeingProfile(db.Model):
#     __tablename__ = 'wellbeingProfiles'
#
#
#     #Forigin Key
#     studentID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('students.studentID'),primary_key=True)
#
#     #reportHistory: so.Mapped[str] = so.mapped_column(sa.String())
#     recommendations: so.Mapped[list[str]] = so.mapped_column(sa.String())
#     wellbeingStatus: so.Mapped[str] = so.mapped_column(sa.String(120))



# Flask-Login integration
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# id@dataclass
# class Professional(db.Model):
#     __tablename__ = 'professionals'
#
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     name: so.Mapped[str] = so.mapped_column(sa.String(128))
#     specialty: so.Mapped[str] = so.mapped_column(sa.String(128))
#     email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
#     available: so.Mapped[bool] = so.mapped_column(default=True)


# @dataclass
# class Message(db.Model):
#     __tablename__ = 'messages'
#
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
#     recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
#     content: so.Mapped[str] = so.mapped_column(sa.Text)
#     #timestamp: so.Mapped[sa.DateTime] = so.mapped_column(default=sa.func.now())




