from sqlalchemy.orm import validates
from hashlib import sha1
from random import randint
import datetime

from zqfa.app import db
from zqfa.models import Base, User
from zqfa.tools import markdown_admin

events_users = db.Table('events_users', Base.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('events.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class Event(Base, db.Model):
    def create_hash(context):
        combination = context.current_parameters['title']+str(randint(0,1000000))
        hash = sha1(combination).hexdigest()
        return hash[0:8]

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(32), nullable=False, unique=True, default=create_hash)

    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    open_for = db.Column(db.Integer, nullable=False, default=2) # 1: public, 2: member, 3: admin
    visibility = db.Column(db.Integer, nullable=False, default=1)  # 1: public, 2: member, 3: admin

    invitation_sent = db.Column(db.DateTime, nullable=True)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    description_html = db.Column(db.Text)
    location = db.Column(db.String(255))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer)

    # TODO: Make sure that in case an event is deleted, the delete is cascaded to the events_users table.
    guests = db.relationship(User, secondary=events_users, backref='events')

    @validates('description')
    def validate_description_html(self, key, field):
        self.description_html = markdown_admin(field)
        return field
