from wtforms import ValidationError
from flask_wtf import Form

from zqfa.models import User
from zqfa.forms.fields import *

class ProfileForm(Form):
    classof = classof
    submit = submit