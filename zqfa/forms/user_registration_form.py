from wtforms import ValidationError, fields
from flask.ext.wtf import Form

from ..models import User
from .fields import *



class UserRegistrationForm(Form):
    classof = classof
    tandc = tandc
    submit = fields.SubmitField('<span class="fa-linkedin"></span> Apply to become a member')