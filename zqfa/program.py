from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required

from datetime import date, timedelta

from zqfa.app import db
from zqfa.models import Event
from zqfa.tools import redirect_back
from zqfa.forms import EventForm, DeleteForm
from zqfa.user import admin_required


bp = Blueprint('program', __name__)


@bp.route('/program/faculty')
def faculty_home():
    return render_template('program/faculty.html')
