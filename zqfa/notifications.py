from flask_mail import Message
from flask import url_for
from . import mail
from .models import User
import json

def event_modified(event):
    try:
        emails = [g.email for g in event.guests]
        if len(emails) > 0:
            html = 'Hello, <br/><br/> the following event has been updated:<br/><br/><strong>' + \
                event.title + '</strong><br/>' + event.description + \
                '<br/>Click <a href="' + url_for('events.show', event_hash=event.hash, _external=True) + \
                '">here</a> to see the events in full on our website.<br/><br/>' + \
                'We are looking forward to seeing you again soon!<br/><br/>' + \
                'Best<br/>Your Qfin Club Team'
            msg = Message(
                subject = 'An event has been updated',
                bcc = emails,
                html = html)
            mail.send(msg)
        return True
    except:
        return False

def event_deleted(event):
    try:
        emails = [g.email for g in event.guests]
        if len(emails) > 0:
            html = 'Hello, <br/><br/> unfortunately, we had to cancel the following event:<br/><br/><strong>' + \
                event.title + '</strong><br/>' + event.description + '<br/><br/>' + \
                'But we are already planning new events, so stay tuned!<br/><br/>' + \
                'We are looking forward to seeing you again soon!<br/><br/>' + \
                'Best<br/>Your Qfin Club Team'
            msg = Message(
                subject = 'An event has been updated',
                bcc = emails,
                html = html)
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
                body = 'See ' + url + ' to activate')
            mail.send(msg)
        return True
    except:
        return False