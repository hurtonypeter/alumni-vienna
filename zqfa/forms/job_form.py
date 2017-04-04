from wtforms import fields, validators
from flask.ext.wtf import Form

from ..models import Event
from .fields import *


class JobForm(Form):

    title = fields.StringField('Title', [validators.DataRequired()])
    company = fields.StringField('Company')
    description = fields.TextAreaField('Description', description='Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown</a> or simple HTML to format the description text. <br> Make sure to add instructions on how to apply for this job.')
    location = fields.StringField('Location')
    url = fields.StringField('URL', description="Link to PDF or job profile page.")

    submit = submit
