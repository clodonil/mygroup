from app import db,app, mail
from flask_mail import Mail, Message
from datetime import datetime
from flask.ext.login import LoginManager, login_user,UserMixin, logout_user
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import INET
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
import hashlib
import os



class User(db.Model):
      id            = db.Column(db.Integer, primary_key=True)
      celular       = db.Column(db.String(100), index=True)
      nome          = db.Column(db.String(100), index=True)
      email         = db.Column(db.String(255), index=True)                
      token         = db.Column(db.String(255), index=True) 
      #status
      # 0 -> Ativo
      # 1 -> Inativo
      # 2 -> Admin
      status        = db.Column(db.Integer)
      date_created  = db.Column(db.DateTime)
      date_modified = db.Column(db.DateTime)
      

      def __repr__(self):
          return '<user %r>' %(self.nome)


      def __init__(self,nome, email, celular):         
          self.nome        = nome
          self.email       = email.lower()
          self.celular     = celular
          self.status      = 0 
          self.token       = self.gerar_token(nome,email)
          self.date_created   = datetime.utcnow()
          self.date_modified  = datetime.utcnow()

          

      def get_id(self):
          return str(self.id)

      def add(self,cat,grupo):
          db.session.add(cat)
          session_commit()
          html = '''
                  Olá {},

                  Você está recebendo esse e-mail por ter cadastrado o seu numero de celular {} no grupo {} online.

                  Estamos enviando a seu senha para administrar a sua conta.

                  Segue:

                  Email: {}              
                  Senha: {}

                  Infinity7 reunindo profissionais.
                  http://www.infinity7.com.br
          '''.format(cat.nome, cat.celular,grupo,cat.email, cat.token)     

          self.send_mail("Token do  Group Whatsapp", [cat.email], html)
          return True

      def update(self):
          self.date_modified  = datetime.utcnow()
          self.token          = self.gerar_token(self.nome, self.email)
          return session_commit()

      def delete(self,cat):
          db.session.delete(cat)
          return session_commit()

      def group_add(self, user, group):
          user.group.append(group)
          return session_commit()

      def group_del(self, user, group):
          user.group.remove(group)
          return session_commit()

      def gerar_token(self,c1,c2):
          return   hashlib.sha224(c1.encode('utf-8') + c2.encode('utf-8') ).hexdigest()  

      def check_token(self,token):
           return self.token == token

      def is_authenticated(self):
          return True

      def is_active(self):
         return True

      def is_anonymous(self):
          return False

      def send_mail(self, subject, recipients, text_body):
           sender = 'clodonil@decoroecsa.com.br'
           msg = Message(subject, sender=sender, recipients=recipients)
           msg.body = text_body           
           with app.app_context():
             mail.send(msg)


#Universal functions

def  session_commit():
      try:
        db.session.commit()
      except SQLAlchemyError as e:             
         db.session.rollback()
         reason=str(e)
         return reason

