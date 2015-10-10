from flask import redirect, url_for
from flask.ext.wtf import Form
from wtforms import fields

from ..tools import get_redirect_target, is_safe_url


class RedirectForm(Form):
    next = fields.HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='page.start', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))