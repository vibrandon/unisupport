from datetime import datetime
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass

# =========================
# 👤 User Model
# =========================
@dataclass
class User(UserMixin, db.Model):
    __abstract__ = True

    # Primary key
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    # Auth + user info
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,unique=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    passwordHash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    email: so.Mapped[str] = so.mapped_column(sa.String(120),unique=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    phoneNumber: so.Mapped[str] = so.mapped_column(sa.String(64),unique=True)
    userType: so.Mapped[str] = so.mapped_column(sa.String(64))

    # Utility methods
    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def isStudent(self):
        return self.userType == 'student'

    def isProfessional(self):
        return self.userType == 'professional'

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role})'

@dataclass
class Student(User):
    __tablename__ = "students"

    degree: so.Mapped[str] = so.mapped_column(sa.String(120))
    address: so.Mapped[str] = so.mapped_column(sa.String(120))

    #Foreign key to professional
    professional_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('professionals.id'), nullable=True)
    professional: so.Mapped["Professional"] = so.relationship(back_populates="students")

@dataclass
class Professional(User):
    __tablename__ = "professionals"

    workplace: so.Mapped[str] = so.mapped_column(sa.String(120))
    expertise: so.Mapped[str] = so.mapped_column(sa.String(120))

    students: so.WriteOnlyMapped[list['Student']] = so.relationship(back_populates="professional")


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




