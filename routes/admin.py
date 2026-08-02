from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import User, Assignment, Message

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.before_request
@login_required
def protect():
    if current_user.role != "admin":
        from flask import abort
        abort(403)

@admin.route("/dashboard")
def dashboard():
    students = User.query.filter_by(role="student").count()
    faculty = User.query.filter_by(role="faculty").count()
    assignments = Assignment.query.count()
    messages = Message.query.count()

    return render_template(
        "admin/dashboard.html",
        students=students,
        faculty=faculty,
        assignments=assignments,
        messages=messages
    )
