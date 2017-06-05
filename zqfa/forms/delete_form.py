from wtforms import fields
from flask_wtf import Form

class DeleteForm(Form):
    submit = fields.SubmitField('Delete')