
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, PasswordField,validators
from wtforms.validators import DataRequired, EqualTo



class PesForm(Form):
     group     = SelectField('Grupos', coerce=int)


class LoginForm(Form):
     login       = StringField('login', validators=[DataRequired()])
     password    = PasswordField('Password',validators=[DataRequired()])


