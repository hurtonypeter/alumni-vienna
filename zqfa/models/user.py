from zqfa.app import db
from zqfa.models import Base
from datetime import datetime


class User(Base, db.Model):
    __tablename__ = 'users'

    # System fields
    id = db.Column(db.Integer, primary_key=True)
    registered = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(255), default='ROLE_USER', nullable=False)

    activated = db.Column(db.Boolean, default=False, nullable=False)

    # Linkedin fields
    linkedin_id = db.Column(db.String(255), nullable=False, unique=True)
    linkedin_token = db.Column(db.String(255), nullable=False, unique=False)
    linkedin_updated = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(255))
    location = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    position = db.Column(db.String(255))
    company = db.Column(db.String(255))
    small_picture_url = db.Column(db.String(255))
    big_picture_url = db.Column(db.String(255))

    positions = db.relationship("UserPosition", order_by="UserPosition.id", backref="user")

    # ZQFA fiels
    classof = db.Column(db.Integer)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.activated

    def is_member(self):
        """ At the moment an alias for activated.
        :return:
        """
        return self.activated

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def has_role(self, role):
        if(self.role):
            if(role in self.role):
                return True
            else:
                return False
        return False

    @property
    def upcoming_events(self):
        upcoming = list()
        if self.events:
            upcoming = [event for event in self.events if event.start_date > datetime.now()]
        return upcoming

    @property
    def name(self):
        if self.firstname and self.lastname:
            return ' '.join([self.firstname, self.lastname])
        return ''
