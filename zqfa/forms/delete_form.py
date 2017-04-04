from wtforms import fields
from flask.ext.wtf import Form

class DeleteForm(Form):
    submit = fields.SubmitField('Delete')