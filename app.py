import os

from flask import Flask, redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

from config import Config
from extensions import db, login_manager


def create_app():

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    app = Flask(
        __name__,
        template_folder=os.path.join(
            BASE_DIR,
            "templates"
        ),
        static_folder=os.path.join(
            BASE_DIR,
            "static"
        )
    )

    # Load configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Initialize login manager
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models AFTER extensions are initialized
    from models import User

    # Import routes
    from routes.auth import (auth)
    from routes.student import (student)
    from routes.faculty import (faculty)
    from routes.admin import (admin)
    from routes.api import (api)
    # Register routes
    app.register_blueprint(auth)
    app.register_blueprint(student)
    app.register_blueprint(faculty)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    # Load logged-in user
    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )

    # Home page
    @app.route("/")
    def index():

        if current_user.is_authenticated:

            if current_user.role == "student":
                return redirect(
                    url_for("student.dashboard")
                )

            elif current_user.role == "faculty":
                return redirect(
                    url_for("faculty.dashboard")
                )

            elif current_user.role == "admin":
                return redirect(
                    url_for("admin.dashboard")
                )

        return redirect(
            url_for("auth.login")
        )

    # Create database tables
    with app.app_context():

        db.create_all()

        # Demo Student
        if not User.query.filter_by(
            email="student@erp.com"
        ).first():

            student = User(
                name="Demo Student",
                email="student@erp.com",
                password=generate_password_hash(
                    "student123"
                ),
                role="student"
            )

            db.session.add(student)

        # Demo Faculty
        if not User.query.filter_by(
            email="faculty@erp.com"
        ).first():

            faculty = User(
                name="Demo Faculty",
                email="faculty@erp.com",
                password=generate_password_hash(
                    "faculty123"
                ),
                role="faculty"
            )

            db.session.add(faculty)

        # Demo Admin
        if not User.query.filter_by(
            email="admin@erp.com"
        ).first():

            admin = User(
                name="ERP Administrator",
                email="admin@erp.com",
                password=generate_password_hash(
                    "admin123"
                ),
                role="admin"
            )

            db.session.add(admin)

        db.session.commit()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )