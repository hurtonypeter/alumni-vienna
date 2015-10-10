from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask.ext.login import current_user, login_required

from datetime import date, timedelta

from . import db
from .models import Event
from .tools import redirect_back
from .forms import EventForm, DeleteForm
from .user import admin_required


bp = Blueprint('events', __name__)


@bp.route('/events')
def index():
    levels = get_access_levels()

    events = Event.query.filter(Event.start_date >= date.today()-timedelta(days=2)).filter(Event.visibility <= levels['visibility']).order_by(Event.start_date).all()
    past_events = Event.query.filter(Event.start_date < date.today()-timedelta(days=2)).filter(Event.visibility <= levels['visibility']).order_by(Event.start_date.desc()).all()

    return render_template('events/index.html', events=events, past_events=past_events, levels=levels)

@bp.route('/event/<string:event_hash>/going/')
@bp.route('/event/<string:event_hash>/going/<string:user_auth_token>')
def going(event_hash, user_auth_token=None):
    event = Event.query.filter_by(hash=event_hash).first()
    if event is None:
        abort(404)

    if not current_user.is_authenticated() and not user_auth_token:
        flash("You don't have access to this area of the website")
        return redirect(url_for('page.home'))

    event.guests.append(current_user)
    db.session.commit()

    flash('Thanks for your reply. You have been added to the guestlist.')
    return redirect(url_for('events.show', event_hash=event_hash))


@bp.route('/event/<string:event_hash>/not_going/')
@bp.route('/event/<string:event_hash>/not_going/<string:user_auth_token>')
def not_going(event_hash, user_auth_token=None):
    event = Event.query.filter_by(hash=event_hash).first()
    if event is None:
        abort(404)

    if not current_user.is_authenticated() and not user_auth_token:
        flash("You don't have access to this area of the website")
        return redirect(url_for('page.home'))


    event.guests.remove(current_user)
    db.session.commit()

    flash('Thanks for your reply. You are no longer on the guestlist.')
    return redirect(url_for('events.show', event_hash=event_hash))


@bp.route('/event/<string:event_hash>/invitation', methods=["GET", "POST"])
@admin_required
def invitation(event_hash):

    event = Event.query.filter_by(hash=event_hash).first()
    if event is None:
        abort(404)

    # TODO Function to send invitations and reminders to event participants


    return redirect(url_for('events.show', event_hash=event_hash))


@bp.route('/event/<string:event_hash>/show')
def show(event_hash):
    event = Event.query.filter_by(hash=event_hash).first()
    if event is None:
        abort(404)

    levels = get_access_levels()

    if levels['visibility'] < event.visibility:
        flash("You don't have access to this page")
        return redirect(url_for('page.home'))
    return render_template('events/show.html', event=event, levels=levels)


@bp.route('/event/new', methods=["GET", "POST"])
@login_required
def new():
    if not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    form = EventForm(request.form)
    if form.validate_on_submit():
        event = Event()
        form.populate_obj(event)
        event.user_id = current_user.id
        db.session.add(event)
        db.session.commit()

        flash('Event successfully created.')
        return redirect(url_for('events.show', event_hash=event.hash))

    return render_template('events/new.html', form=form)


@bp.route('/event/<string:event_hash>/edit', methods=["GET", "POST"])
@login_required
def edit(event_hash):
    if not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    event = Event.query.filter_by(hash=event_hash).first()
    if event is None:
        abort(404)

    form = EventForm(request.form, event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()

        flash('Event successfully updated.')
        return redirect(url_for('events.show', event_hash=event.hash))

    return render_template('events/new.html', form=form)


@bp.route('/event/<string:event_hash>/delete', methods=["POST"])
@login_required
def delete(event_hash):
    if not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    event = Event.query.filter_by(hash=event_hash).first()
    if event is None:
        abort(404)

    form = DeleteForm(request.form, event)
    if form.validate_on_submit():
        db.session.delete(event)
        db.session.commit()

        flash('Event successfully removed.')
        return redirect(url_for('events.index'))

    flash('Invalid CSRF token')
    return redirect_back()


def get_access_levels():
    open_for = 1
    visibility = 1

    if current_user.is_authenticated() and current_user.is_active():
        open_for = 2
        visibility = 2

        if current_user.has_role('ROLE_ADMIN'):
            open_for = 3
            visibility = 3
    return {'visibility':visibility, 'open_for':open_for}
