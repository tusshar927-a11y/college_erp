from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from models import User, Attendance, Assignment, Message
from extensions import db

api = Blueprint("api", __name__, url_prefix="/api")


# =========================================
# LOGIN
# =========================================

@api.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    if not check_password_hash(user.password, password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    })


# =========================================
# STUDENT ATTENDANCE
# =========================================

@api.route("/student/attendance/<int:student_id>", methods=["GET"])
def student_attendance(student_id):

    records = Attendance.query.filter_by(
        student_id=student_id
    ).order_by(
        Attendance.date.desc()
    ).all()

    subjects = {}

    for record in records:

        subject = record.subject

        if subject not in subjects:

            subjects[subject] = {
                "subject": subject,
                "total": 0,
                "present": 0,
                "absent": 0,
                "percentage": 0
            }

        subjects[subject]["total"] += 1

        if record.status.lower() == "present":
            subjects[subject]["present"] += 1
        else:
            subjects[subject]["absent"] += 1

    for subject in subjects:

        total = subjects[subject]["total"]
        present = subjects[subject]["present"]

        if total > 0:
            subjects[subject]["percentage"] = round(
                (present / total) * 100
            )

    total_classes = len(records)

    total_present = sum(
        1
        for record in records
        if record.status.lower() == "present"
    )

    overall_percentage = 0

    if total_classes > 0:
        overall_percentage = round(
            (total_present / total_classes) * 100
        )

    return jsonify({
        "success": True,
        "overall_percentage": overall_percentage,
        "total_classes": total_classes,
        "total_present": total_present,
        "subjects": list(subjects.values())
    })


# =========================================
# STUDENT ASSIGNMENTS
# =========================================

@api.route("/student/assignments", methods=["GET"])
def student_assignments():

    assignments = Assignment.query.order_by(
        Assignment.due_date.asc()
    ).all()

    result = []

    for assignment in assignments:

        result.append({
            "id": assignment.id,
            "title": assignment.title,
            "subject": assignment.subject,
            "description": assignment.description,
            "due_date": assignment.due_date.strftime("%Y-%m-%d"),
            "faculty_id": assignment.faculty_id
        })

    return jsonify({
        "success": True,
        "assignments": result
    })


# =========================================
# STUDENT MESSAGES
# =========================================

@api.route("/student/messages/<int:student_id>", methods=["GET"])
def student_messages(student_id):

    messages = Message.query.filter_by(
        receiver_id=student_id
    ).order_by(
        Message.created_at.desc()
    ).all()

    result = []

    for message in messages:

        sender = User.query.get(message.sender_id)

        result.append({
            "id": message.id,
            "subject": message.subject,
            "message": message.message,
            "is_read": message.is_read,
            "sender": sender.name if sender else "Unknown",
            "created_at": message.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return jsonify({
        "success": True,
        "messages": result
    })


# =========================================
# FACULTY - STUDENTS
# =========================================

@api.route("/faculty/students", methods=["GET"])
def faculty_students():

    students = User.query.filter_by(
        role="student"
    ).all()

    result = []

    for student in students:

        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email
        })

    return jsonify({
        "success": True,
        "students": result
    })


# =========================================
# FACULTY - MARK ATTENDANCE
# =========================================

@api.route("/faculty/attendance", methods=["POST"])
def mark_attendance():

    data = request.get_json()

    student_id = data.get("student_id")
    subject = data.get("subject")
    date = data.get("date")
    status = data.get("status")

    if not all([
        student_id,
        subject,
        date,
        status
    ]):
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    from datetime import datetime

    attendance_date = datetime.strptime(
        date,
        "%Y-%m-%d"
    ).date()

    record = Attendance(
        student_id=student_id,
        subject=subject,
        date=attendance_date,
        status=status
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Attendance saved successfully",
        "attendance_id": record.id
    })


# =========================================
# FACULTY - VIEW ATTENDANCE
# =========================================

@api.route("/faculty/attendance/<int:student_id>", methods=["GET"])
def faculty_view_attendance(student_id):

    records = Attendance.query.filter_by(
        student_id=student_id
    ).order_by(
        Attendance.date.desc()
    ).all()

    result = []

    for record in records:

        result.append({
            "id": record.id,
            "student_id": record.student_id,
            "subject": record.subject,
            "date": record.date.strftime("%Y-%m-%d"),
            "status": record.status
        })

    return jsonify({
        "success": True,
        "attendance": result
    })