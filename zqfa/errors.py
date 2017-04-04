from flask import Blueprint, render_template, redirect, url_for, request
from flask.ext.login import current_user, flash

from .tools import get_redirect_target
from . import csrf

bp = Blueprint('errors', __name__)


@bp.app_errorhandler(404)
def not_found(err):
    code = 403
    title = 'Not Found'
    message = "Sorry, but the requested resource could not be found."
    return render_template('errors/show.html', code=code, title=title, message=message), code

@bp.app_errorhandler(403)
def forbidden(err):
    code = 403
    if not current_user.is_authenticated():
        target = get_redirect_target()
        if not target:
            target = request.url
        flash('You do not have access to this resource, please login.', 'error')
        return redirect(url_for('user.login', next=target), code=code)
    else:

        title = 'Access denied'
        message = "Sorry, but you don't have access to this resource."
        return render_template('errors/show.html', code=code, title=title, message=message), code

@bp.app_errorhandler(500)
def internal_server_error(err):
    code = 500
    title = 'Internal Server Error'
    message = "Sorry, but we could not handle your request at the moment. Please try again later."
    return render_template('errors/show.html', code=code, title=title, message=message), code


@csrf.error_handler
def csrf_error(reason):
     code = 400
     title = 'Bad Request - CSRF Token not valid'
     message = "The Cross-Site-Request-Forgery token was not valid or missing. If you were direct to" \
               "this page from an external website, this could have been an malicious attempt to manipulate" \
               "your content on ZQFA.<br><br>" \
               "If not, please reload the previous page and try again."
     return render_template('errors/show.html', code=code, title=title, message=message), code