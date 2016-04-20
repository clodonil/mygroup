from app import db
from datetime import datetime
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import INET
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

import os


member = db.Table('member',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class Group(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      titulo        = db.Column(db.String(100), index=True)
      descricao     = db.Column(db.String(255), index=True)          
      #status
      # 0 -> Ativo
      # 1 -> Inativo
      # 2 -> Lotado
      status        = db.Column(db.Integer)
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)


      # Relacionamento many to many (user x group)
      members       = db.relationship('User', secondary=member, backref=db.backref('group', lazy='dynamic'))
      

      def __repr__(self):
          return '<Group %r>' %(self.titulo)


      def __init__(self,titulo, descricao):         
          self.titulo         = titulo
          self.descricao      = descricao
          self.status         = 0 
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()

          

      def get_id(self):
          return str(self.id)

      def add(self,cat):
          db.session.add(cat)
          return session_commit ()

      def update(self):
          self.date_modified  = datetime.utcnow()
          return session_commit()

      def delete(self,cat):
          db.session.delete(cat)
          return session_commit()





#Universal functions

def  session_commit():
      try:
        db.session.commit()
      except SQLAlchemyError as e:             
         db.session.rollback()
         reason=str(e)
         return reason

