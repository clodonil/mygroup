from flask import render_template, flash, redirect, request,session, redirect, Blueprint, url_for
from werkzeug import secure_filename
from app import db
from flask.ext.login import login_required, current_user
from datetime import date
from app.group.forms import GroupForm
from app.group.model import Group
#from flask.ext.login import login_required
import os



group = Blueprint('group',__name__)

@group.route('/index')
@group.route('/')
#@login_required
def index():
    groups = Group.query.all()    
    return render_template('group/index.html',title='Lista de clientes',groups=groups)


@group.route('/new', methods=['GET','POST'])
#@login_required
def new():
    form = GroupForm()    
    if form.validate_on_submit():
       emp = Group(
                      form.titulo.data,
                      form.descricao.data                     
                    )

       emp.add(emp)
       return redirect(url_for('inscrever.index'))
    return render_template('group/new.html',title='Cadastro de grupos',form=form)

@group.route("/edit/<int:emp_id>", methods = ["GET","POST"])
# @login_required
def edit(emp_id):
    emp = Group.query.get(emp_id)    
    form = GroupForm(obj=emp)     
    if form.validate_on_submit():
        emp.titulo    = form.titulo.data
        emp.descricao = form.descricao.data
        emp.status    = form.status.data
        emp.update()
        return redirect(url_for('group.index'))
    return render_template("group/edit.html",title='Alteração de Grupos', form=form)


@group.route("/delete/<int:emp_id>", methods = ["GET","POST"])
# @login_required
def delete(emp_id):
    emp = Group.query.get(emp_id)    
    emp.delete(emp)
    return redirect(url_for('group.index'))    

@group.context_processor
def utility_processor():
    def len_group(group_id ):
        group = Group.query.get(group_id)
        return len(group.members)
   
    return dict(len_group=len_group)


# @group.context_processor    
# def dados():
#     usuario = Usuario.query.get(current_user.id)
#     hoje    = date.today()
#     return dict(usuario = usuario.nome,hoje=hoje)



