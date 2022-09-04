
from socket import socket
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_admin import Admin

db=SQLAlchemy()#instance from class SQLALCHEMY 
migrate=Migrate()
mail = Mail()
admin=Admin()