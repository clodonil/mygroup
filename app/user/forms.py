
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, FloatField, IntegerField, DateField,TextAreaField, SelectField, FileField, TextField,validators
from wtforms.validators import DataRequired
from datetime import datetime


class UserForm(Form):
     nome        = StringField('Nome', validators=[DataRequired()])
     email       = StringField('Email', validators=[DataRequired()])
     celular     = StringField('celular', validators=[DataRequired()])     
     status      = SelectField('Status', choices=[('0','Ativo'),('1','Inativo')], default=0)


class PesForm(Form):
     group     = SelectField('Grupos', coerce=int)     