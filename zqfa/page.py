from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import current_user, logout_user, login_required

bp = Blueprint('page', __name__)


@bp.route('/')
def start():
    if current_user.is_authenticated() and current_user.registered:
        return redirect(url_for('page.home'))
    elif ((current_user.is_authenticated() and not current_user.registered)
          or session.get('registration') == 1
          or session.get('registration') == 2):
        logout_user()
        session['registration'] = None
    return home()

@bp.route('/home')
def home():
    return render_template('page/home.html')

@bp.route('/about')
def about():
    return render_template('page/about.html')
    
@bp.route('/shop')
def shop():
    return render_template('page/shop.html')

@bp.route('/terms')
def terms():
    return render_template('page/terms.html')

@bp.route('/privacy')
def privacy():
    return render_template('page/privacy.html')

@bp.route('/success')
@login_required
def success():
    return render_template('page/success.html')
