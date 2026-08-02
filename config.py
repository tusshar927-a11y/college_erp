import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost/college_erp"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
