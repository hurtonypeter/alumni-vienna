from wtforms import fields, validators
from flask.ext.wtf import Form

from ..models import Event
from .fields import *



class EventForm(Form):

    title = fields.StringField('Title', [validators.Required()])
    description = fields.TextAreaField('Description', description="Use Markdown or HTML to format the description text.")
    location = fields.StringField('Location')

    start_date = fields.DateTimeField('When?', [validators.Required()], format='%Y-%m-%d %H:%M')
    end_date = fields.DateTimeField('until? (optional)',  [validators.Optional()], format='%Y-%m-%d %H:%M')


    open_for = fields.SelectField('Open for', choices = [(1, "Everyone"), (2, "Only for members")], coerce=int) # 1: public, 2: member, 3: admin
    visibility = fields.SelectField("Visibility", choices = [(1, "Everyone"), (2, "Only for members"), (3, "Only for admins")], coerce=int)

    submit = submit