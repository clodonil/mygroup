#coding: utf-8

import os
from flask import Flask, Blueprint, redirect,url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir
from flask_mail import Mail, Message


app = Flask(__name__)
app.config.from_object('config')

# Banco de Dados
db = SQLAlchemy(app)


# Servidor de Email
mail = Mail(app)


@app.route('/')
def index():
    #return redirect(url_for('auth.login'))
    return redirect(url_for('group.index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Autenticação
login_manager = LoginManager()
login_manager.init_app(app)

# Modulos
#from app.auth.controllers import auth
from app.group     import group
from app.user      import user
from app.inscrever import inscrever



#app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(group, url_prefix='/group')
app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(inscrever, url_prefix='/inscrever')