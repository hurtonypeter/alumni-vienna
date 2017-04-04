from .. import db
from . import Base
from datetime import datetime


class UserPosition(Base, db.Model):
    __tablename__ = 'user_positions'

    id = db.Column(db.Integer, primary_key=True)
    linkedin_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    company = db.Column(db.String(255))
    linkedin_company_id = db.Column(db.Integer)
    title = db.Column(db.String(255))

    start_year = db.Column(db.Integer)
    start_month= db.Column(db.Integer)

    end_year = db.Column(db.Integer)
    end_month = db.Column(db.Integer)

    is_current = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #user = db.relationship('User', backref=db.backref('user_positions', cascade="all, delete-orphan"))