import hashlib
from mailchimp3 import MailChimp
from . import mailchimp_api

def check_connection():
    try:
        print mailchimp_api
        mailchimp_api.lists.all(get_all=True, fields = "lists.name,lists.id")
        return True
    except:
        print "Mailchimp API not available."
        return False

def generate_merge_vars(user):
    merge_vars = {'FNAME': user.firstname,
                  'LNAME': user.lastname,
                  'CLASSOF': user.classof }
    return merge_vars

def get_subscriber_hash_from_email(user_email):
    return hashlib.md5(user_email.lower().encode('utf-8')).hexdigest()

def subscribe(list_id, user, merge_vars=None):
    data = { "email_address": user.email, "status": "subscribed"}
    try:
        mailchimp_api.lists.members.create(list_id=list_id, data = data)
        return True
    except:
        return False

def user_on_list(list_id, user_email):
    user_hash = get_subscriber_hash_from_email(user_email)
    try:
        resp = mailchimp_api.lists.members.get(list_id, subscriber_hash=user_hash, fields = "status")
        return resp['status'] == 'subscribed' if True else False
    except:
        return False

def unsubscribe(list_id, user):
    user_hash = get_subscriber_hash_from_email(user.email)
    try:
        mailchimp_api.lists.members.delete(list_id=list_id, subscriber_hash=user_hash)
        return True
    except:
        return False

def unsubscribe_all(user):
    lists = get_lists()
    for list in lists:
        unsubscribe(list['id'], user)

def subscribe_all(user):
    lists = get_lists()
    for list in lists:
        subscribe(list['id'], user)

def get_lists():
    lists = mailchimp_api.lists.all(get_all=True, fields = "lists.name,lists.id")

    return lists['lists']

def update_email(old_email, new_email):
    user_hash = get_subscriber_hash_from_email(old_email)
    patch_data = { 'status': 'subscribed', 'email_address': 'asd@gmail.com' }
    lists = get_lists()
    try:
        for list in lists:
            if user_on_list(list['id'], old_email):
                mailchimp_api.lists.members.update(list_id = list['id'], subscriber_hash = user_hash, data = patch_data )
        return True
    except:
        return False
