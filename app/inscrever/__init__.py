from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db,login_manager
from flask.ext.login import login_user,logout_user,LoginManager, UserMixin, current_user, login_required
from datetime import date
from .forms import PesForm, LoginForm
from app.group.model import Group
from app.user.model import User
import os



inscrever = Blueprint('inscrever',__name__)


@inscrever.route('/', methods = ["GET","POST"])
def index():
    if current_user.is_active and current_user.id != 1:
       return redirect(url_for('user.perfil'))
    
    print(current_user.is_active)

    form = PesForm()
    form.group.choices = [(h.id,h.titulo) for h in Group.query.filter(Group.id != 1).all()]
    groups = Group.query.filter(Group.id != 1).all()    

    if form.validate_on_submit():
        group_id = form.group.data
        return redirect(url_for('user.new', emp_id = group_id))

    return render_template('inscrever/index.html',title='Pesquisa de Grupo',form=form, groups=groups)

@inscrever.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       login    = form.login.data
       password = form.password.data

       user = User.query.filter_by(email=login.lower()).first()

       if user and user.check_token(password):       
          login_user(user)
          session['usuario'] = user.id
          flash('Logged in successfully')
          return redirect(url_for('user.perfil'))
       else:
         flash('usuario ou senha invalido')

    return render_template('inscrever/login.html',title='Autenticação', form=form)


@inscrever.route('/logout')
@login_required
def logout():
    logout_user()
    session['usuario'] = ''
    return redirect(url_for('inscrever.index'))

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('inscrever.index'))	


@inscrever.context_processor
def utility_processor():
    def len_group(group_id ):
        group = Group.query.get(group_id)
        return len(group.members)

    def admin(id):
        admin = Group.query.get(1)
        return id in [x.id for x in admin.members]

        
   
    return dict(len_group=len_group, admin=admin)

    

# @inscrever.context_processor    
# def dados():
#     usuario = Usuario.query.get(current_user.id)
#     hoje    = date.today()
#     return dict(usuario = usuario.nome,hoje=hoje)



