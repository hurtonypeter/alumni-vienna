from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import current_user, login_required
from flask_wtf import Form
from flask_mail import Message
from wtforms import fields

import newsletter
from zqfa.app import db, mail
from zqfa.models import User, UserPosition
from zqfa.forms import SubscriptionsForm, ProfileForm
from zqfa.tools import redirect_back
from zqfa.user import user_active_required, admin_required
from zqfa.events import get_access_levels


bp = Blueprint('members', __name__)


@bp.route('/members')
@user_active_required
def index():
    not_active = []
    if current_user.has_role('ROLE_ADMIN'):
        not_active = User.query.filter_by(activated=False)

    members = User.query.filter_by(activated=True)

    """
    # Attach current position to members
    query.filter(User.name.in_(['ed', 'wendy', 'jack']))

    # works with query objects too:
    query.filter(User.name.in_(
            session.query(User.name).filter(User.name.like('%ed%'))
    ))
    """

    for member in members:
        member.current_position = UserPosition.query.filter_by(user_id=member.id, is_current=True)

    return render_template('members/index.html', members = members, not_active=not_active)


@bp.route('/member/<int:user_id>/activate', methods=['POST'])
@admin_required
def activate(user_id):
    ''' Activates the user account and sends a welcome message '''

    form = Form(request.form)
    if form.validate_on_submit():
        u = User.query.get_or_404(user_id)
        u.activated = True
        db.session.commit()

        msg = Message("ZQFA: Application accepted. Welcome!", recipients=[u.email])
        msg.html = render_template('members/email_welcome.html', user=u)
        mail.send(msg)

        # Subscribe to mailinglists
        newsletter.subscribe_all(u)

        flash('User has been activated, a welcome message has been sent and he has been subscribed to all newsletters.')
    else:
        flash('Invalid CSRF Token')
    return redirect_back()


@bp.route('/member/<int:user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate(user_id):
    form = Form(request.form)
    if form.validate_on_submit():
        u = User.query.get_or_404(user_id)
        u.activated = False
        db.session.commit()

        newsletter.unsubscribe_all(u)

        flash('User has been deactivated and unsubscribed from all newsletter.')
    else:
        flash('Invalid CSRF Token')
    return redirect_back()


@bp.route('/member/<int:user_id>/delete', methods=["POST"])
@admin_required
def delete(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()

    flash(u.name+' has been removed from the database.', 'success')

    return redirect(url_for('members.index'))

@bp.route('/profile', defaults={'user_id': None})
@bp.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    if not current_user.is_active() and user_id != current_user.id:
        flash('You have to wait until you application has been approved to access this area.', 'error')
        return redirect_back()

    user = User.query.get_or_404(user_id)

    if not user.is_active() and user_id != current_user.id and not user.has_role('ROLE_ADMIN'):
        flash('The member exists, but is not yet activated and can therefore his profile is not yet available.', 'error')
        return redirect_back()

    return render_template('members/profile.html', user=user, levels = get_access_levels())


@bp.route('/subscriptions', methods=['GET', 'POST'])
@user_active_required
def subscriptions():
    class F(SubscriptionsForm):
        pass

    class Data():
        pass

    if newsletter.check_connection() is False:
        flash('Service at the moment not available. Please try again later.')
        return redirect_back()

    # Dynamically create form
    lists = newsletter.get_lists()
    lists_id = []
    for subscription_list in lists:
        lists_id.append(subscription_list['id'])
        on_list = newsletter.user_on_list(subscription_list['id'], current_user.email)
        setattr(F, subscription_list['id'], fields.BooleanField(subscription_list['name']))
        setattr(Data, subscription_list['id'], on_list)

    form = F(request.form, Data)

    if form.validate_on_submit():
        for subscription_list, value in form.data.iteritems():
            if subscription_list in lists_id:
                if value != getattr(Data, subscription_list):
                    if value:
                        newsletter.subscribe(subscription_list, current_user)
                    else:
                        newsletter.unsubscribe(subscription_list, current_user)
        flash('Your subscriptions have been successfully updated.')

    return render_template('members/subscriptions.html', form=form)


@bp.route('/profile/<int:user_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit(user_id):
    if current_user.id != user_id and not current_user.has_role('ROLE_ADMIN'):
        abort(403)

    user = User.query.get_or_404(user_id)

    form = ProfileForm(request.form, obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.commit()

        flash('You have your profile successfully edited.', 'success')
        return redirect(url_for('members.profile', user_id=current_user.id))

    return render_template('user/edit.html', form=form, user=user)
