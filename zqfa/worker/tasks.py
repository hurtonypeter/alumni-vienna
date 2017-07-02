from mailchimp3 import MailChimp
from datetime import date, timedelta
from zqfa.models import Event, Job
from zqfa.app import mailchimp_api, app

import json

footer = 'We are looking forward to seeing you again soon!<br/><br/>' + \
         'Best<br/>Your Qfin Club Team'
from_name = "QFinClub"
reply_to = "qfinclub@wu.ac.at"

def events_newsletter(events):
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub events",
            "from_name": from_name,
            "reply_to": reply_to
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
        "html": 'Hello! <br /><br />' + \
                events_list(events) + footer
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
            "reply_to": reply_to
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
        "html": 'Hello! <br /><br />' + \
                jobs_list(jobs) + footer
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
            "reply_to": reply_to
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
        "html": 'Hello! <br /><br />' + \
                events_list(events) + jobs_list(jobs) + footer
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
        

# ----------------------------------------------------------
##  Helpers
# ----------------------------------------------------------

def events_list(events):
    if len(events) > 0:
        return 'The following events have been added this week: ' + \
                events_to_html_list(events) + 'Click <a href="https://qfinclub.com/events">here</a> ' + \
                'to see all evenets in full on our website.<br/><br/>'
    else:
        return ''

def events_to_html_list(events):
    text = "<ul>"
    for event in events:
        text += "<li><strong>" + event.start_date.strftime('%A, %b %d at %H:%M') +"</strong> - " + event.title + "</li>"
    return text + "</ul>"

def jobs_list(jobs):
    if len(jobs):
        return 'The following jobs have been added this week: ' + \
                jobs_to_html_list(jobs) + 'Click <a href="https://qfinclub.com/jobs">here</a> ' + \
                'to see all jobs in full on our website.<br/><br/>'
    else:
        return ''

def jobs_to_html_list(jobs):
    text = "<ul>"
    for job in jobs:
        text += "<li>" + job.title + "</li>"
    return text + "</ul>"
