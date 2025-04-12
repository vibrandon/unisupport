from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy.orm import relationship
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

    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', cascade='all, delete-orphan',
                                    backref='sender')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', cascade='all, delete-orphan',
                                        backref='receiver')

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


class Student(User):
    __tablename__ = 'students'
    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)
    degree: so.Mapped[str] = so.mapped_column(sa.String(120),nullable=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(256),nullable=True)
    surveys: so.Mapped[list['studentSurvey']] = relationship(back_populates='student', cascade='all, delete-orphan')
    wellbeingProfile: so.Mapped['wellbeingProfile'] = relationship(back_populates='student')

    pid: so.Mapped[int] = so.mapped_column(nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


@dataclass
class Professional(User):
    __tablename__ = 'professionals'
    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), primary_key=True)
    workplace: so.Mapped[str] = so.mapped_column(sa.String(120),nullable=True)
    specialty: so.Mapped[str] = so.mapped_column(sa.String(120),nullable=True)
    surveys: so.Mapped['professionalSurvey'] = relationship(back_populates='professional', cascade='all, delete-orphan')

    __mapper_args__ = {
        "polymorphic_identity": "professional",
    }

# Flask-Login integration
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



@dataclass()
class Chatbot(db.Model):
    __tablename__ = 'MessagesWithChatbot'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    message: so.Mapped[str] = so.mapped_column(sa.Text)
    ChatbotMessage: so.Mapped[bool] = so.mapped_column(default=False)
    TimeOfMessage: so.Mapped[datetime] = so.mapped_column(sa.DateTime,default=sa.func.now())
    #user: so.Mapped['User'] = relationship(back_populates='MessagesWithChatbot')

    def __repr__(self):
        return f'Chatbot(id={self.id}, user_id={self.user_id}, ChatbotMessage={self.ChatbotMessage})'

class Admin(User):
    __tablename__ = 'admins'
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

class wellbeingProfile(db.Model):
    __tablename__ = 'wellbeingProfiles'
    #Foreign Key
    studentID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('students.id'),primary_key=True)
    student: so.Mapped['Student'] = relationship(back_populates='wellbeingProfile')
    #reportHistory: so.Mapped[str] = so.mapped_column(sa.String())
    recommendations: so.Mapped[list[str]] = so.mapped_column(sa.String())
    wellbeingStatus: so.Mapped[str] = so.mapped_column(sa.String(120))

class survey(db.Model):
    __tablename__ = 'surveys'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    type: so.Mapped[str] = so.mapped_column(sa.String(50))
    # change questions from a list into a dictionary with {question:answer,question:answer} pairs
    questions: so.Mapped[list[str]] = so.mapped_column(sa.String())
    #timestamp added
    timestamp: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, default=datetime.now)

    #implementation of getQuestions function
    def getQuestions(self):
        return self.questions

    #polymorphism so that studentSurvey and professionalSurvey can inherit
    __mapper_args__ = {
        "polymorphic_identity": "surveys",
        "polymorphic_on": type,
    }

# fixed inheritance: class studentSurvey(db.Model):
class studentSurvey(survey):
    __tablename__ = 'studentSurveys'
    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('surveys.id'), primary_key=True)
    studentID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('students.id'), index=True)
    student: so.Mapped['Student'] = relationship(back_populates='surveys')
    #polymorphism to inherit from survey class
    __mapper_args__ = {
        "polymorphic_identity": "studentSurvey",
    }

class professionalSurvey(survey):
    __tablename__ = 'professionalSurveys'
    id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('surveys.id'), primary_key=True)
    professionalID: so.Mapped[int] = so.mapped_column(sa.ForeignKey('professionals.id'), index=True)
    professional: so.Mapped['Professional'] = relationship(back_populates='surveys')
    __mapper_args__ = {
        "polymorphic_identity": "professionalSurvey",
    }

# Flask-Login integration
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))





