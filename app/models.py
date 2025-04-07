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
    __tablename__ = 'users'

    # Primary key
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    # Auth + user info
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,nullable=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,nullable=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="User")
    address: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)

    # Utility methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email}, role={self.role})'

# Flask-Login integration
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

@dataclass
class Professional(db.Model):
    __tablename__ = 'professionals'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    specialty: so.Mapped[str] = so.mapped_column(sa.String(128))
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    available: so.Mapped[bool] = so.mapped_column(default=True)


@dataclass
class Message(db.Model):
    __tablename__ = 'messages'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    content: so.Mapped[str] = so.mapped_column(sa.Text)
    #timestamp: so.Mapped[sa.DateTime] = so.mapped_column(default=sa.func.now())

@dataclass
class AdjustmentRequest(db.Model):
    __tablename__ = 'adjustment_requests'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    reason: so.Mapped[str] = so.mapped_column(sa.Text)
    status: so.Mapped[str] = so.mapped_column(sa.String(20), default="Pending")  # Pending / Approved / Denied
    submitted_at: so.Mapped[datetime] = so.mapped_column(default=sa.func.now())
