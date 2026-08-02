from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Assignment, Attendance, Message, User
from extensions import db


student = Blueprint(
    "student",
    __name__,
    url_prefix="/student"
)


@student.before_request
@login_required
def protect():

    if current_user.role != "student":
        from flask import abort
        abort(403)


# -----------------------------------------
# STUDENT DASHBOARD
# -----------------------------------------

@student.route("/dashboard")
def dashboard():

    assignments = Assignment.query \
        .order_by(Assignment.due_date.asc()) \
        .limit(5).all()

    attendance = Attendance.query \
        .filter_by(
            student_id=current_user.id
        ).all()

    messages = Message.query \
        .filter_by(
            receiver_id=current_user.id
        ) \
        .order_by(
            Message.created_at.desc()
        ) \
        .limit(5).all()

    total = len(attendance)

    present = sum(
        1
        for a in attendance
        if a.status == "Present"
    )

    attendance_pct = (
        round((present / total) * 100)
        if total
        else 0
    )

    return render_template(
        "student/dashboard.html",
        assignments=assignments,
        messages=messages,
        attendance_pct=attendance_pct
    )


# -----------------------------------------
# SUBJECT-WISE ATTENDANCE
# -----------------------------------------

@student.route("/attendance")
def attendance():

    records = Attendance.query \
        .filter_by(
            student_id=current_user.id
        ) \
        .order_by(
            Attendance.date.desc()
        ).all()

    subjects = {}

    for record in records:

        subject = record.subject

        if subject not in subjects:

            subjects[subject] = {
                "total": 0,
                "present": 0,
                "absent": 0,
                "percentage": 0
            }

        subjects[subject]["total"] += 1

        if record.status == "Present":

            subjects[subject]["present"] += 1

        else:

            subjects[subject]["absent"] += 1


    # Calculate percentage for each subject

    for subject in subjects:

        total = subjects[subject]["total"]

        present = subjects[subject]["present"]

        subjects[subject]["percentage"] = round(
            (present / total) * 100
        ) if total else 0


    # Overall attendance

    total_classes = len(records)

    total_present = sum(
        1
        for record in records
        if record.status == "Present"
    )

    overall_percentage = round(
        (total_present / total_classes) * 100
    ) if total_classes else 0


    return render_template(
        "student/attendance.html",
        subjects=subjects,
        records=records,
        overall_percentage=overall_percentage,
        total_classes=total_classes,
        total_present=total_present
    )


# -----------------------------------------
# STUDENT MESSAGES
# -----------------------------------------

@student.route("/messages")
def messages():

    messages = Message.query \
        .filter_by(
            receiver_id=current_user.id
        ) \
        .order_by(
            Message.created_at.desc()
        ).all()

    return render_template(
        "student/messages.html",
        messages=messages
    )