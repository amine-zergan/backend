from flask import Flask 
from flask_restx import Api
from .views import book
from .utilis import db,migrate
from .models import Book,UrlPath
from .models import UserModel,Framework
from .settings import config_dict
from flask_admin import Admin
from .utilis import mail,admin




#ceate function  instance from object flask 
def create_app(config=config_dict['dev']):
    app=Flask(__name__)
    app.config.from_object(config)
    api=Api(app)
    mail.init_app(app)
    admin.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    api.add_namespace(book,path="/books")

    @app.shell_context_processor
    def make_shell_context():
        return{
            "db":db,
            "User":UserModel,
            "Book":Book,
            "Framework":Framework,
            "UrlPath":UrlPath
        }
    return app