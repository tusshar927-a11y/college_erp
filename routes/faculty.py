from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from models import Assignment, Message, User, Attendance
from extensions import db

faculty = Blueprint("faculty", __name__, url_prefix="/faculty")

@faculty.before_request
@login_required
def protect():
    if current_user.role != "faculty":
        from flask import abort
        abort(403)

@faculty.route("/dashboard")
def dashboard():
    assignments = Assignment.query.filter_by(faculty_id=current_user.id).order_by(Assignment.created_at.desc()).all()
    students = User.query.filter_by(role="student").all()
    messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).limit(5).all()
    return render_template("faculty/dashboard.html", assignments=assignments, students=students, messages=messages)

@faculty.route("/assignments", methods=["GET", "POST"])
def assignments():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        subject = request.form.get("subject", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date")

        if not title or not subject or not due_date:
            flash("Please fill all required fields.", "danger")
        else:
            assignment = Assignment(
                title=title,
                subject=subject,
                description=description,
                due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
                faculty_id=current_user.id
            )
            db.session.add(assignment)
            db.session.commit()
            flash("Assignment posted successfully.", "success")
            return redirect(url_for("faculty.assignments"))

    assignments = Assignment.query.filter_by(faculty_id=current_user.id).order_by(Assignment.due_date.asc()).all()
    return render_template("faculty/assignments.html", assignments=assignments)

@faculty.route("/students")
def students():
    students = User.query.filter_by(role="student").order_by(User.name.asc()).all()
    return render_template("faculty/students.html", students=students)
@faculty.route("/faculty/attendance", methods=["GET", "POST"])
@login_required
def attendance():

    # Only faculty can access attendance management
    if current_user.role != "faculty":
        return redirect(url_for("index"))

    students = User.query.filter_by(
        role="student"
    ).order_by(
        User.name
    ).all()

    if request.method == "POST":

        subject = request.form.get(
            "subject",
            ""
        ).strip()

        date_string = request.form.get(
            "date",
            ""
        )

        if not subject or not date_string:
            flash(
                "Please select a subject and date.",
                "danger"
            )

            return redirect(
                url_for("faculty.attendance")
            )

        try:

            attendance_date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            flash(
                "Invalid date.",
                "danger"
            )

            return redirect(
                url_for("faculty.attendance")
            )

        # Remove previous attendance for the same
        # subject and date before saving the new list.
        Attendance.query.filter_by(
            subject=subject,
            date=attendance_date
        ).delete()

        # Save attendance for every student
        for student in students:

            status = request.form.get(
                f"status_{student.id}",
                "Absent"
            )

            attendance_record = Attendance(
                student_id=student.id,
                subject=subject,
                date=attendance_date,
                status=status
            )

            db.session.add(
                attendance_record
            )

        db.session.commit()

        flash(
            "Attendance saved successfully!",
            "success"
        )

        return redirect(
            url_for("faculty.attendance")
        )

    return render_template(
        "faculty/attendance.html",
        students=students
    )