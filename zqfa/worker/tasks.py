from mailchimp3 import MailChimp
from flask import render_template
from datetime import date, timedelta
from zqfa.models import Event, Job
from zqfa.app import mailchimp_api, app

from_name = "QFin Club"

def events_newsletter(events):
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub events",
            "from_name": from_name,
            "reply_to": app.config['MAILCHIMP_REPLY_TO']
        },
        "recipients": {
            "list_id": app.config['MAILCHIMP_EVENTS_NEWSLETTER']
        }
    }
    resp_camp = mailchimp_api.campaigns.create(data_camp)
    id_camp = resp_camp['id']
    if not id_camp:
        raise Exception(resp_camp['title'] + " " + resp_camp['detail'])

    data_cont = {
        "html": render_template('newsletters/events_newsletter.html', events=events)
    }
    mailchimp_api.campaigns.content.update(campaign_id=id_camp, data=data_cont)
    mailchimp_api.campaigns.actions.send(campaign_id=id_camp)

    return True

def jobs_newsletter(jobs):
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub jobs",
            "from_name": from_name,
            "reply_to": app.config['MAILCHIMP_REPLY_TO']
        },
        "recipients": {
            "list_id": app.config['MAILCHIMP_JOBS_NEWSLETTER']
        }
    }
    resp_camp = mailchimp_api.campaigns.create(data_camp)
    id_camp = resp_camp['id']
    if not id_camp:
        raise Exception(resp_camp['title'] + " " + resp_camp['detail'])

    data_cont = {
        "html": render_template('newsletters/jobs_newsletter.html', jobs=jobs)
    }
    mailchimp_api.campaigns.content.update(campaign_id=id_camp, data=data_cont)
    mailchimp_api.campaigns.actions.send(campaign_id=id_camp)

    return True

def combined_newsletter(jobs, events):
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub events and jobs",
            "from_name": from_name,
            "reply_to": app.config['MAILCHIMP_REPLY_TO']
        },
        "recipients": {
            "list_id": app.config['MAILCHIMP_COMBINED_NEWSLETTER']
        }
    }
    resp_camp = mailchimp_api.campaigns.create(data_camp)
    id_camp = resp_camp['id']
    if not id_camp:
        raise Exception(resp_camp['title'] + " " + resp_camp['detail'])
    
    data_cont = {
        "html": render_template('newsletters/combined_newsletter.html', jobs=jobs, events=events)
    }
    mailchimp_api.campaigns.content.update(campaign_id=id_camp, data=data_cont)
    mailchimp_api.campaigns.actions.send(campaign_id=id_camp)
    return True

def send_newsletter():
    compare_date = date.today() - timedelta(days=7)
    jobs = Job.query.filter(Job.created >= compare_date).all()
    events = Event.query.filter(Event.created >= compare_date).order_by(Event.start_date).all()

    if len(jobs) > 0:
        jobs_newsletter(jobs)
    if len(events) > 0:
        events_newsletter(events)
    if len(jobs) > 0 or len(events) > 0:
        combined_newsletter(jobs, events)
        
