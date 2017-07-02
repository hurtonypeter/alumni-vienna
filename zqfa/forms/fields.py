from wtforms import fields, validators
from datetime import date

classof = fields.SelectField('Class of', [validators.Required()],
                              choices=[(0,'')]+[(x,x) for x in range(2002,date.today().year + 3)], coerce=int,
                              description='The year you started your studies officially in the program.')


tandc = fields.BooleanField('I accept the <a href="/terms">terms and conditions</a>.', [validators.Required(message="This field is mandatory.")])

login = fields.SubmitField('Login')
next = fields.SubmitField('Next')
submit = fields.SubmitField('Submit')