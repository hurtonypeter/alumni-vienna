import os
from mailchimp3 import MailChimp
from zqfa.models import User, UserPosition, Event, Job

import json

mailchimp_api = MailChimp(
    os.getenv('MAILCHIMP_USERNAME', 'hurtonypeter'),
    os.getenv('MAILCHIMP_APIKEY', '1bf5a40b84aaf2eae8e4b5e3436d4fe3-us15'))

footer = '<br/><br/>We are looking forward to seeing you again soon!<br/><br/>' + \
         'Best<br/>Your Qfin Club Team'
from_name = "QFinClub"
reply_to = "hurtonypeter@gmail.com"

def events_newsletter():
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub events",
            "from_name": from_name,
            "reply_to": reply_to
        },
        "recipients": {
            "list_id": os.getenv('MAILCHIMP_EVENTS_NEWSLETTER', '54ef41b266')
        }
    }
    resp_camp = mailchimp_api.campaigns.create(data_camp)
    id_camp = resp_camp['id']

    data_cont = {
        "html": 'Hello! <br /><br />' + \
                events_list() + footer
    }
    mailchimp_api.campaigns.content.update(campaign_id=id_camp, data=data_cont)
    mailchimp_api.campaigns.actions.send(campaign_id=id_camp)

    return True

def jobs_newsletter():
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub jobs",
            "from_name": from_name,
            "reply_to": reply_to
        },
        "recipients": {
            "list_id": os.getenv('MAILCHIMP_JOBS_NEWSLETTER', '54ef41b266')
        }
    }
    resp_camp = mailchimp_api.campaigns.create(data_camp)
    id_camp = resp_camp['id']

    data_cont = {
        "html": 'Hello! <br /><br />' + \
                jobs_list() + footer
    }
    mailchimp_api.campaigns.content.update(campaign_id=id_camp, data=data_cont)
    mailchimp_api.campaigns.actions.send(campaign_id=id_camp)

    return True

def combined_newsletter():
    data_camp = {
        "type": "regular",
        "settings": {
            "subject_line": "QFinClub events and jobs",
            "from_name": from_name,
            "reply_to": reply_to
        },
        "recipients": {
            "list_id": os.getenv('MAILCHIMP_COMBINED_NEWSLETTER', '54ef41b266')
        }
    }
    resp_camp = mailchimp_api.campaigns.create(data_camp)
    id_camp = resp_camp['id']

    data_cont = {
        "html": 'Hello! <br /><br />' + \
                events_list() + '<br /><br />' + jobs_list() + footer
    }
    mailchimp_api.campaigns.content.update(campaign_id=id_camp, data=data_cont)
    mailchimp_api.campaigns.actions.send(campaign_id=id_camp)
    return True

def send_newsletter():
    #lists = mailchimp_api.lists.all(get_all=True, fields="lists.name,lists.id")
    #jobs = Job.query.filter(Job.show_until >= date.today())
    #events_newsletter()
    print "yay"
    return None

# ----------------------------------------------------------
##  Helpers
# ----------------------------------------------------------

def events_list():
    return 'The following events have been added this week: ' + \
            events_to_html_list() + 'Click <a href="https://qfinclub.com/events">here</a> ' + \
            'to see all evenets in full on our website.'

def events_to_html_list():
    return "<ul><li>event1</li></ul>"

def jobs_list():
    return 'The following jobs have been added this week: ' + \
            jobs_to_html_list() + 'Click <a href="https://qfinclub.com/jobs">here</a> ' + \
            'to see all jobs in full on our website.'

def jobs_to_html_list():
    return "<ul><li>job1</li></ul>"

def log(szoveg):
    f = open("/home/logs/log.txt", 'a')
    f.write("\n")
    f.write(json.dumps(szoveg, indent=4))
    f.close()
    return None

