from wtforms import ValidationError, fields
from flask_wtf import Form

from zqfa.models import User
from zqfa.forms.fields import *



class UserRegistrationForm(Form):
    classof = classof
    tandc = tandc
    submit = fields.SubmitField('<span class="fa-linkedin"></span> Apply to become a member')