from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask.ext.login import current_user
from flask_mail import Message

from datetime import date, timedelta, datetime

from . import db, mail
from .models import Job
from .tools import redirect_back
from .forms import JobForm, DeleteForm
from .user import user_active_required

bp = Blueprint('jobs', __name__)


@bp.route('/jobs')
@user_active_required
def index():
    jobs = Job.query.filter(Job.show_until >= date.today()).order_by(Job.show_until.desc()).all()
    expired_user_jobs = Job.query.filter(Job.show_until < date.today()).filter(Job.user_id == current_user.id).order_by(Job.show_until.desc()).all()
    return render_template('jobs/index.html', jobs = jobs, expired_user_jobs = expired_user_jobs)


@bp.route('/job/<string:job_hash>/show')
@user_active_required
def show(job_hash):
    job = Job.query.filter_by(hash=job_hash).first()
    if job is None:
        abort(404)

    return render_template('jobs/show.html', job=job)


@bp.route('/job/new', methods=["GET", "POST"])
@user_active_required
def new():
    form = JobForm(request.form)
    if form.validate_on_submit():
        job = Job()
        form.populate_obj(job)
        job.user_id = current_user.id
        db.session.add(job)
        db.session.commit()

        flash('Job successfully created.')

        # TODO: Make notification configurable
        message = 'See '+url_for('jobs.show', job_hash=job.hash, _external=True)
        subject = '[ZQFA] New job posting'
        recipient = 'kevin@zqfa.ch'
        msg = Message(subject=subject, recipients=[recipient], body=message, sender=("ZQFA", "info@zqfa.ch"))
        #mail.send(msg)
        return redirect(url_for('jobs.show', job_hash=job.hash))

    return render_template('jobs/new.html', form=form)


@bp.route('/job/<string:job_hash>/edit', methods=["GET", "POST"])
@user_active_required
def edit(job_hash):
    job = Job.query.filter_by(hash=job_hash).first()
    if job is None:
        abort(404)

    if current_user.id != job.user_id and not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    form = JobForm(request.form, job)
    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()

        flash('Job successfully updated.')
        return redirect(url_for('jobs.show', job_hash=job.hash))

    return render_template('jobs/new.html', form=form, job=job)


@bp.route('/job/<string:job_hash>/repost', methods=["GET"])
@user_active_required
def repost(job_hash):
    job = Job.query.filter_by(hash=job_hash).first()
    if job is None:
        abort(404)

    if current_user.id != job.user_id and not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    job.show_until = datetime.now()+timedelta(days=30)
    db.session.commit()

    flash('Job is again on the job board for the next 30 days.')
    return redirect(url_for('jobs.show', job_hash=job.hash))


@bp.route('/job/<string:job_hash>/delete', methods=["POST"])
@user_active_required
def delete(job_hash):
    job = Job.query.filter_by(hash=job_hash).first()
    if job is None:
        abort(404)

    if current_user.id != job.user_id and not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    form = DeleteForm(request.form, job)
    if form.validate_on_submit():
        db.session.delete(job)
        db.session.commit()

        flash('Job successfully removed.')
        return redirect(url_for('jobs.index'))

    flash('Invalid CSRF token')
    return redirect_back()
