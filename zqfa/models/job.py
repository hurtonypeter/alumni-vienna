import random
import string
from datetime import datetime, timedelta

from sqlalchemy.orm import validates

from .. import db
from ..tools import markdown_user
from . import Base


def create_hash(context):
    hash = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in xrange(12))
    return hash

def in_30_days():
    return datetime.now()+timedelta(days=30)

class Job(Base, db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(32), nullable=False, unique=True, default=create_hash)

    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.now)

    show_until = db.Column(db.DateTime, default=in_30_days)

    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    description = db.Column(db.Text)
    description_html = db.Column(db.Text)
    location = db.Column(db.String(255))
    url = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref("jobs", cascade="all, delete-orphan"))


    @validates('description')
    def validate_description_html(self, key, field):
        self.description_html = markdown_user(field)
        return field

    @property
    def nice_url(self):
        stripped = self.url.replace('http://', '').replace('https://', '')
        if len(stripped) > 30:
            return stripped[0:30] + '...'
        else:
            return stripped
