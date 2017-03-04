#!venv/bin/python
from xd import db
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    file = db.Column(db.String(128), default=None)
    email = db.Column(db.String(64), default=None)
    xd_id = db.Column(db.Integer, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
