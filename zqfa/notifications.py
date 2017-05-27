from flask_mail import Message
from . import mail
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