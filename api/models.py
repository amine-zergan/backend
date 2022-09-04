from .utilis import db,admin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin





class FileView(FileAdmin):
    can_mkdir=False
    can_delete_dirs=False
    can_download=True
    


class UserModel(db.Model): #  class UserModel extends db.Model{il va nous fournir les outils aui va translater vers requete sql}
    __tablename__="users" #create Table users if not exists ()
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    create_at=db.Column(db.DateTime(),default=datetime.utcnow())
    books = db.relationship('Book',backref='book', lazy=True)
    frameworks = db.relationship('Framework',backref='framework', lazy=True)
    images = db.relationship('UrlPath',backref='image', lazy=True)

    def __repr__(self):
        return f"user {self.username}"
    def save(self):
        db.session.add(self)
        db.session.commit()


class Book(db.Model):
    __tablename__="books"
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    author=db.Column(db.String(70),nullable=False)
    description=db.Column(db.String(300),nullable=True)
    create=db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
        nullable=False)

    def __repr__(self) :
        return f"book is {self.title}"

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Framework(db.Model):
    __tablename__="framworks"
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(50),nullable=False,unique=True)
    description=db.Column(db.String())
    date_creat_at=db.Column(db.DateTime(),default=datetime.utcnow())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
        nullable=False)
    def __repr__(self) :
        return f"frameware used {self.name}"

    
    def save(self):
        db.session.add(self)
        db.session.commit()
  
class UrlPath(db.Model):
    __tablename__="images"
    id=db.Column(db.Integer(),primary_key=True)
    file_name=db.Column(db.String(100),nullable=False,unique=True)
    url_name=db.Column(db.String(200),nullable=False,)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
        nullable=False)
    def __repr__(self) :
        return f"image used {self.file_name}"
    def save(self):
        db.session.add(self)
        db.session.commit()
path="/Users/aminemejri/Desktop/Apiflask/api/upload"
#interfaace de l"admin pour gerer la database
admin.add_view(ModelView(Book,db.session))
admin.add_view(ModelView(UserModel,db.session))
admin.add_view(ModelView(Framework,db.session))
admin.add_view(ModelView(UrlPath,db.session))
admin.add_view(FileView(path, '/upload/', name='Files',))