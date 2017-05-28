from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from flask_mail import Message
from flask.ext.login import current_user, login_user, logout_user
from flask_oauthlib.client import OAuth

from . import login_manager, db, mail
from .models import User, UserPosition
from .forms import UserRegistrationForm
from .tools import redirect_back
import newsletter
<<<<<<< HEAD
import notifications
=======
>>>>>>> 5b7b8c8e686f82f470310bac23e2d803a0dc9044

from random import randint
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound


bp = Blueprint('user', __name__)

linkedin = None
login_manager.login_view = "user.login"

'''
# How the LinkedIn sign in and sign up work

If the user is not authenticated he has the option to sign in/up.

## Sign up: /become-member
The become a member info page is shown, where a user has to specify
his starting year with the master and accepting the terms of condition.

As soon as the become-a-meber form validates, the classof year is saved
in a session and the user is redirect to authenticate via LinkedIn and
authorize ZQFA to access some of his data (authorize method).

The authorize method checks the LinkedIn authentication asks for the
permissions needed and:

1. Redirects the user back to become-a-member in case no user exists yet
in the database.
2. Logs the user in, in case a user with the respective LinkedIn ID and  is
 already available in the database.

As soon as the user is authenticated via LinkedIn and therefore the value
'linkedin_token' is set in the session, the user is created by the
become_member method. The respective fields we are interested in are set via
the method update_linkedin_fields. After this process the user is logged in,
but not yet activated, meaning that is_authenticated() calls will return false
until the row active in the user table is set to 1.

## Login
A user who tries to login, is directly sent to linkedin for authentication
and authorization.

In case the user is registered, his profile fields are updated via a call to
update_linkedin_fields and he is logged in and sent to members.index.

In case no user account has been found, he is sent to the become-member page,
where a user account is created if he accepts the terms and conditions and
enters his "classof" year.

'''

@bp.route('/become-member', methods=['GET', 'POST'])
def become_member():

    if current_user.is_authenticated():
        flash('You are already registered.')
        redirect(url_for('members.index'))


    if 'classof' not in session:
        form = UserRegistrationForm(request.form, obj=current_user)
        if not form.validate_on_submit():
            return render_template('user/become_member.html', form=form)
        else:
            session['classof'] = form.classof.data

    if 'linkedin_token' not in session:
        # Send to Linkedin Auth
        return redirect(url_for('user.login'))

    linkedin_id = session['linkedin_id']

    try:
        user = User.query.filter_by(linkedin_id=linkedin_id).one()
    except MultipleResultsFound:
        flash('There has been an error, please try again later', 'error')
        return redirect('page.home')
    except NoResultFound:
        # User not yet registered, so create it!
        user = User()
        # System fields
        user.registered = datetime.now()
        user.last_login = datetime.now()
        # Linkedin fields
        update_linkedin_fields(user)
        # ZQFA fields
        user.classof = session['classof']
        # Commit to DB
        db.session.add(user)
        db.session.commit()

        login_user(user, force=True)
        user.last_login = datetime.now()
        db.session.commit()
        session.pop('classof', None)

        # Inform admin
<<<<<<< HEAD
        notifications.admin_notification_new_user(user)
=======
        msg = 'See '+url_for('members.index', _external=True)+' to activate.'
        send_mail('info@zqfa.ch', '[ZQFA] New user '+user.name, msg)
>>>>>>> 5b7b8c8e686f82f470310bac23e2d803a0dc9044

        return redirect(url_for('page.success'))

    flash('You are already registered.', 'error')
    return redirect(url_for('members.index'))


def update_linkedin_fields(user, token=None):

    if token is None:
        token = session['linkedin_token'][0]

    profile = linkedin.get('people/~:(id,first-name,last-name,location:(name),industry,positions,picture-url,picture-urls::(original),public-profile-url,email-address)', token=(token,))

    status_code = profile.data.get('status')

    if not status_code:
        user.linkedin_updated = datetime.now()
        user.linkedin_token = token
        user.linkedin_id = profile.data.get('id', randint(0,100000))

        email_old = user.email
        email_new = profile.data.get('emailAddress', '')

        if email_new:
            user.email = email_new

        # Handle mailchimp subscription
        if user.activated and email_old != user.email and newsletter.check_connection():
            if not email_old:
                # Till now, email was empty, subscribe user to all newsletters
                newsletter.subscribe_all(user)
            else:
                # E-Mail changed, so update it in mailchimp
                newsletter.update_email(email_old, user.email)

        user.firstname = profile.data.get('firstName', '')
        user.lastname = profile.data.get('lastName', '')
        user.linkedin_url = profile.data.get('publicProfileUrl', '')
        user.location = profile.data.get('location', {}).get('name', '')
        user.industry = profile.data.get('industry', '')

        if profile.data.get('positions', {}).get('_total', 0) > 0:
            #import pprint
            #pp = pprint.PrettyPrinter(indent=6)

            ups = [item[0] for item in db.session.query(UserPosition.linkedin_id).filter_by(user_id=user.id).all()]
            for positions in profile.data.get('positions', {}).get('values', {}):
                linkedin_id = positions.get('id', None)

                if linkedin_id in ups:
                    ups.remove(linkedin_id)

                if linkedin_id:
                    up = UserPosition.query.filter_by(linkedin_id=linkedin_id, user_id=user.id).first()
                    new = False

                    if up is None:
                        up = UserPosition()
                        up.linkedin_id = linkedin_id
                        new = True

                    up.company = positions.get('company', {}).get('name', '')
                    up.linkedin_company_id = positions.get('company', {}).get('id', None)

                    up.is_current = positions.get('company', {}).get('id', None)
                    up.title = positions.get('title', '')
                    up.start_month = positions.get('startDate', {}).get('month', None)
                    up.start_year = positions.get('startDate', {}).get('year', None)
                    up.end_month = positions.get('endDate', {}).get('month', None)
                    up.end_year = positions.get('endDate', {}).get('year', None)
                    up.is_current = positions.get('isCurrent', False)
                    up.user_id = user.id

                    # Add entry only if there is something
                    if up.company and up.title:
                        if new:
                            db.session.add(up)
                        db.session.commit()

            # Delete positions no longer in the LinkedIn Profile
            if ups:
                for linkedin_id in ups:
                    up = UserPosition.query.filter_by(linkedin_id=linkedin_id).first()
                    db.session.delete(up)
                    db.session.commit()

        user.small_picture_url = profile.data.get('pictureUrl', '')
        pictureUrls = profile.data.get('pictureUrls', {}).get('values', {})
        user.big_picture_url = pictureUrls[0] if pictureUrls else ''

        return True
    else:
        print profile.data
        return False


@bp.route('/linkedin', methods=['GET','POST'])
def linkedin():
    url = request.form.get('linkedin')
    if url is None:
        url = 'people/~:(id,first-name,last-name,industry)'
    raw = linkedin.get(url)
    data = raw.data
    return render_template('user/linkedin.html', data = data, url=url)


@bp.route('/login')
def login():
    return linkedin.authorize(callback=url_for('user.authorized', _external=True, _scheme='https'))


@bp.route('/logout')
def logout():
    session.pop('linkedin_token', None)
    session.pop('linkedin_id', None)
    session.pop('classof', None)

    if current_user.is_authenticated():
        logout_user()

    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('page.home'))


@bp.route('/_oauth/linkedin/authorized')
def authorized():
    resp = linkedin.authorized_response()
    if resp is None or not resp['access_token']:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    token = resp['access_token']
    session['linkedin_token'] = (token,'')

    profile = linkedin.get('people/~:(id,email-address)')
    linkedin_id = profile.data['id']
    session['linkedin_id'] = linkedin_id
    # Try to login the user
    try:
        user = User.query.filter_by(linkedin_id=linkedin_id).one()
    except MultipleResultsFound:
        flash('There has been an error, please try again later', 'error')
        return redirect('page.home')
    except NoResultFound:
        # Register
        return redirect(url_for('user.become_member'))

    login_user(user, force=True)
    user.last_login = datetime.now()
    update_linkedin_fields(user)
    db.session.commit()
    flash('You have been successfully logged in.')
    return redirect_back()


def get_linkedin_oauth_token():
    return session.get('linkedin_token')


def change_linkedin_query(uri, headers, body):
    auth = headers.pop('Authorization')
    headers['x-li-format'] = 'json'
    if auth:
        auth = auth.replace('Bearer', '').strip()
        if '?' in uri:
            uri += '&oauth2_access_token=' + auth
        else:
            uri += '?oauth2_access_token=' + auth
    return uri, headers, body


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def send_mail(recipient, subject, message):
    """
    Shortcut to send an email from ZQFA. An info text why someone is receiving this email (because he is a registered user), is automatically added. Use therefor only to write emails to registered users and for really important system messages.
    :param recipient: E-Mail address of the recipient
    :param subject: Subject of the email
    :param message: Message text of the email
    :return: boolean
    """
    message = message + '\n\n\n' \
                        '--\n' \
                        'You get this email because you are registered on ZQFA (www.zqfa.ch). As this is a system message you cannot unsubscribe from it.\n'

    msg = Message(subject=subject, recipients=[recipient], body=message, sender=("ZQFA", "info@zqfa.ch"))
    return mail.send(msg)



def user_active_required(func):
    '''
    If you decorate a view with this, it will ensure that the current user is
    activated (as a member) and authenticated before calling the actual view. For
    example:

        @app.route('/post')
        @user_active_required
        def post():
            pass

    :param func: The view function to decorate.
    :type func: function
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated() or not current_user.is_active():
            flash('To access this page, your application has first to be reviewed.')
            return redirect_back()
        return func(*args, **kwargs)
    return decorated_view


def admin_required(func):
    '''
    If you decorate a view with this, it will ensure that the current user is
    activated (as a member) and authenticated before calling the actual view. For
    example:

        @app.route('/post')
        @admin_required
        def post():
            pass

    :param func: The view function to decorate.
    :type func: function
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated() or not current_user.has_role('ROLE_ADMIN'):
            flash("You have no permission to access this page.")
            return redirect_back()
        return func(*args, **kwargs)
    return decorated_view


@bp.route('/user/update/all', defaults={'user_id': None})
@bp.route('/user/update/<int:user_id>')
@admin_required
def run_update(user_id):
    if user_id is None:
        users = User.query.all()
    else:
        users = [User.query.get_or_404(user_id)]

    for user in users:
        print 'Updating '+user.name
        if update_linkedin_fields(user, token=user.linkedin_token):
            print '  successfull'
        else:
            print '  error (probably expired or revoked token)'


    flash('Users updated')
    return redirect_back()



def setUp(app):
    global linkedin
    oauth = OAuth(app)
    linkedin = oauth.remote_app(
        'linkedin',
        consumer_key=app.config['LINKEDIN_CONSUMER_KEY'],
        consumer_secret=app.config['LINKEDIN_CONSUMER_SECRET'],
        request_token_params={
            'scope': 'r_emailaddress r_basicprofile',
            'state': 'RandomString',
        },
        base_url='https://api.linkedin.com/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
        authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
    )
    linkedin.tokengetter(get_linkedin_oauth_token)
    linkedin.pre_request = change_linkedin_query

    app.register_blueprint(bp)

