from flask_mail import Message
from flask import url_for
from . import mail
from .models import User
import json

def event_modified(event):
    try:
        emails = [g.email for g in event.guests]
        if len(emails) > 0:
            msg = Message(
                subject = 'An event has been updated',
                recipients=emails,
                body = 'salalala ',
                sender= 'qfinclub@gmail.com')
            mail.send(msg)
        return True
    except:
        return False

def event_deleted(event):
    try:
        emails = [g.email for g in event.guests]
        if len(emails) > 0:
            msg = Message(
                subject = 'An event has been canceled',
                recipients=emails,
                body = 'nyehehe ',
                sender= 'qfinclub@gmail.com')
            mail.send(msg)
        return True
    except:
        return False

def admin_notification_new_user(user):
    try:
        admins = User.query.filter_by(role='ROLE_ADMIN')
        emails = [a.email for a in admins]
        if len(emails) > 0:
            url = url_for('members.index', _external=True)
            msg = Message(
                subject = 'New user',
                recipients=emails,
                body = 'See ' + url + ' to activate',
                sender= 'qfinclub@gmail.com')
            mail.send(msg)
        return True
    except:
        return False