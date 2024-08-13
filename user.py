from flask_login import UserMixin
from . import db_access


class User(db_access.Model, UserMixin):
    id = db_access.Column(
        db_access.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    email = db_access.Column(db_access.String(100), unique=True)
    password = db_access.Column(db_access.String(100))
    name = db_access.Column(db_access.String(1000))
    role = db_access.Column(db_access.String(100))
