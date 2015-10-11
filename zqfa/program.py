from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask.ext.login import current_user, login_required

from datetime import date, timedelta

from . import db
from .models import Event
from .tools import redirect_back
from .forms import EventForm, DeleteForm
from .user import admin_required


bp = Blueprint('program', __name__)


@bp.route('/program/faculty')
def faculty_home():
    return render_template('program/faculty.html')