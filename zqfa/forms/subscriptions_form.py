from wtforms import fields
from flask.ext.wtf import Form


class SubscriptionsForm(Form):
    submit = fields.SubmitField('Update')