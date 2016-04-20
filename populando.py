#!env/bin/python

from app.user.model import User
from app.group.model import Group

group = Group('admin','grupo dos administradores')
group.add(group)


user = User('clodonil','clodonil@gmail.com','(11)97987987987')
user.add(user, group.titulo)
user.group_add(user, group)

user.status = 3

user.update()
