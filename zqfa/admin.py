from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required

from zqfa.tools import redirect_back
from zqfa.user import user_active_required, admin_required
from zqfa.worker import tasks

import traceback

bp = Blueprint('admin', __name__)

@bp.route('/admin/newsletters')
@admin_required
def newsletters():
    return render_template('admin/newsletters.html')

@bp.route('/admin/newsletters', methods=["POST"])
@admin_required
def send_newsletters():
    try:
        tasks.send_newsletter()
        flash('Newsletters successfully sent.')
    except Exception as ex:
        traceback.print_exc()
        flash('Something went wrong! Can not send the newsletters. ' + ex.message)
    return redirect_back()