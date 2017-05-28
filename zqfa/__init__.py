from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.heroku import Heroku
from flask_sslify import SSLify
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask_wtf.csrf import CsrfProtect

<<<<<<< HEAD
from mailchimp3 import MailChimp
=======
import mailchimp
>>>>>>> 5b7b8c8e686f82f470310bac23e2d803a0dc9044

bootstrap = Bootstrap()
mail = Mail()
csrf = CsrfProtect()

mailchimp_api = None

def create_app():
    from os import environ

    app = Flask(__name__)
    SSLify(app)

    try:
        # Local machine during development
        app.config.from_pyfile('../config.py')
    except:
        # In case of foreman or directly on Heroku
        app.config['DEBUG'] = bool(int(environ.get('DEBUG', False)))
        app.debug = app.config['DEBUG']
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        app.config['MANDRILL_USERNAME'] = environ.get('MANDRILL_USERNAME')
        app.config['MANDRILL_APIKEY'] = environ.get('MANDRILL_APIKEY')

        app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
        app.config['MAIL_PORT'] = environ.get('MAIL_PORT')
        app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')
        app.config['MAIL_USE_TLS'] = bool(int(environ.get('MAIL_USE_TLS', False)))

<<<<<<< HEAD
        app.config['MAILCHIMP_USERNAME'] = environ.get('MAILCHIMP_USERNAME')
=======
>>>>>>> 5b7b8c8e686f82f470310bac23e2d803a0dc9044
        app.config['MAILCHIMP_APIKEY'] = environ.get('MAILCHIMP_APIKEY')

        app.config['LINKEDIN_CONSUMER_KEY'] = environ.get('LINKEDIN_CONSUMER_KEY')
        app.config['LINKEDIN_CONSUMER_SECRET'] = environ.get('LINKEDIN_CONSUMER_SECRET')

        app.config['GOOGLE_ANALYTICS'] = environ.get('GOOGLE_ANALYTICS')

        malformed_uri = environ['CLEARDB_DATABASE_URL']
        # because cleardb adds a query parameter ?reconnect=true, we have
        # to remove it for the driver to work
        correct_uri = malformed_uri.split("?")[0]
        app.config['SQLALCHEMY_DATABASE_URI'] = correct_uri
        heroku.init_app(app)


    app.config['MAIL_USERNAME'] = app.config['MANDRILL_USERNAME']
    app.config['MAIL_PASSWORD'] = app.config['MANDRILL_APIKEY']

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    bootstrap.init_app(app)

    mail.init_app(app)
    csrf.init_app(app)

    global mailchimp_api
<<<<<<< HEAD
    mailchimp_api = MailChimp(app.config['MAILCHIMP_USERNAME'], app.config['MAILCHIMP_APIKEY'])
=======
    mailchimp_api = mailchimp.Mailchimp(app.config['MAILCHIMP_APIKEY'])
>>>>>>> 5b7b8c8e686f82f470310bac23e2d803a0dc9044


    ADMINS = ['gereon@zqfa.ch']
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler(mailhost=app.config['MAIL_SERVER'],
                                   fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                                   toaddrs=ADMINS, subject='YourApplication Failed',credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']), secure=app.config['MAIL_USE_TLS'])
        mail_handler.setLevel(logging.WARNING)
        app.logger.addHandler(mail_handler)


    @app.template_filter('check_string')
    def check_string(obj):
        return isinstance(obj, basestring)

    import tools
    tools.setUp(app)

    import errors
    app.register_blueprint(errors.bp)

    import user
    user.setUp(app)

    import page
    app.register_blueprint(page.bp)

    import jobs
    app.register_blueprint(jobs.bp)

    import members
    app.register_blueprint(members.bp)

    import events
    app.register_blueprint(events.bp)

    import models
    models.setUp(app)

    # add sentry if we are in production and it is configured
    if app.config.get('SENTRY_DSN') and not app.config.get('DEBUG'):
        from raven.contrib.flask import Sentry
        sentry = Sentry(app)

    with app.app_context():
        db.create_all()

    return app

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_message = "Please login!"
login_manager.login_message_category = "info"

bcrypt = Bcrypt()
heroku = Heroku()