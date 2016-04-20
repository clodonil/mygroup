from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from flask.ext.login import login_required, current_user
from datetime import date
from .forms import UserForm,PesForm
from .model import User
from app.group.model import Group

#from flask.ext.login import login_required
import os



user = Blueprint('user',__name__)

@user.route('/index')
@user.route('/')
@login_required
def index():

    users = User.query.all()    
    return render_template('user/index.html',title='Lista de clientes',users=users)


@user.route('/new/<int:emp_id>', methods=['GET','POST'])
def new(emp_id):
    # pesquisa o grupo 
    
    form  = UserForm()        
    if form.validate_on_submit():
       
       group = Group.query.get(emp_id)
       emp = User(
                      form.nome.data,
                      form.email.data,
                      form.celular.data
                    )

       if emp.add(emp, group.titulo):
          flash("Erro ao criar usuário")
       emp.group_add(emp, group)

       return redirect(url_for('inscrever.index'))
    return render_template('user/new.html',title='Cadastro de grupos',form=form)

@user.route("/edit/<int:emp_id>", methods = ["GET","POST"])
@login_required
def edit(emp_id):
    emp = User.query.get(emp_id)    
    form = UserForm(obj=emp)     
    if form.validate_on_submit():
        emp.nome    = form.nome.data
        emp.email   = form.email.data
        emp.celular = form.celular.data
        emp.status  = form.status.data
        emp.update()
        return redirect(url_for('user.index'))
    return render_template("user/edit.html",title='Alteração de Grupos', form=form)


@user.route("/delete/<int:emp_id>", methods = ["GET","POST"])
@login_required
def delete(emp_id):
    emp = User.query.get(emp_id)    
    emp.delete(emp)
    return redirect(url_for('user.index'))    

@user.route("/list/<int:group_id>") 
def list(group_id):
   group = Group.query.get(group_id)
   return render_template("user/list.html",title='Lista de Usuário por Grupo', group=group)

@user.route('/perfil', methods = ["GET","POST"]) 
@login_required
def perfil():

    user = User.query.get(session['usuario'])

    form = PesForm()
    form.group.choices = [(h.id,h.titulo) for h in Group.query.filter(Group.id != 1).all()]
    groups = Group.query.all()    

    if form.validate_on_submit():
        group_id = form.group.data
        group = Group.query.get(group_id)        
        user.group_add(user, group)
        return redirect(url_for('user.perfil'))
    return render_template("user/perfil.html",title='Perfil do Usuario', user=user,form=form)    

@user.route("/sair_group/<int:emp_id>", methods = ["GET","POST"])
@login_required
def sair_group(emp_id):
    user  = User.query.get(session['usuario'])    
    group = Group.query.get(emp_id)   
    user.group_del(user,group)
    return redirect(url_for('user.perfil'))    


# @user.context_processor    
# def dados():
#     usuario = Usuario.query.get(current_user.id)
#     hoje    = date.today()
#     return dict(usuario = usuario.nome,hoje=hoje)



