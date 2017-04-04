import mailchimp
from . import mailchimp_api


def check_connection():
    try:
        mailchimp_api.helper.ping()
    except mailchimp.Error:
        print "Mailchimp API not available."
        return False
    return True

def generate_merge_vars(user):
    merge_vars = {'FNAME': user.firstname,
                  'LNAME': user.lastname,
                  'CLASSOF': user.classof }
    return merge_vars

def subscribe(list_id, user, merge_vars=None):
    if not merge_vars:
        merge_vars = generate_merge_vars(user)
    try:
        mailchimp_api.lists.subscribe(list_id, {'email': user.email}, double_optin=False, merge_vars=merge_vars)
    except mailchimp.ListAlreadySubscribedError:
        return True
    except mailchimp.Error:
        return False
    return True

def user_on_list(list_id, user_email):
    result = mailchimp_api.lists.member_info(list_id, {'emails':{'email':user_email}})
    on_list = (result['error_count'] == 0 and result['data'][0]['status'] in ['subscribed', 'pending'])
    return on_list

def unsubscribe(list_id, user):
    if user_on_list(list_id, user.email):
        mailchimp_api.lists.unsubscribe(list_id, {'email':user.email}, send_goodbye=False, send_notify=False)
        return True
    else:
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
    mc_lists = mailchimp_api.lists.list()
    num_lists = int(mc_lists['total'])

    lists = []
    for i in range(num_lists):
        lists.append({'id': mc_lists['data'][i]['id'], 'name': mc_lists['data'][i]['name']})
    return lists

def update_email(old_email, new_email):
    merge_vars = {'new-email': old_email}
    lists = get_lists()
    for list in lists:
        if user_on_list(list['id'], old_email):
            # Replace email
            mailchimp_api.lists.update_member(list['id'], {'email': old_email}, merge_vars=merge_vars)
    return True

