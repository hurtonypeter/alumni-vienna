from wtforms import ValidationError
from flask.ext.wtf import Form

from ..models import User
from .fields import *

class ProfileForm(Form):
    classof = classof
    submit = submit