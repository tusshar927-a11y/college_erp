from datetime import datetime
from flask_login import UserMixin

from extensions import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    subject = db.Column(
        db.String(200),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id]
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id]
    )


class Assignment(db.Model):

    __tablename__ = "assignments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    subject = db.Column(
        db.String(120),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    due_date = db.Column(
        db.Date,
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Attendance(db.Model):

    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    subject = db.Column(
        db.String(120),
        nullable=False
    )

    date = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        nullable=False
    )