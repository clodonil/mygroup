
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, TextField,validators
from wtforms.validators import DataRequired
from datetime import datetime


class GroupForm(Form):
     titulo         = StringField('Titulo', validators=[DataRequired()])
     descricao      = StringField('Descrição', validators=[DataRequired()])
     status         = SelectField('Status', choices=[('0','Ativo'),('1','Inativo')], default=0)

