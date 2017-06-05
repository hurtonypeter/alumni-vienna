from wtforms import fields
from flask_wtf import Form


class SubscriptionsForm(Form):
    submit = fields.SubmitField('Update')