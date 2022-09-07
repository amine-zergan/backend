


import os
import datetime
from venv import create
from flask_restx import Resource,Namespace,fields
from flask import request ,jsonify,Flask
from .models import Book, Framework,UrlPath,UserModel
from werkzeug.utils import secure_filename
from flask import send_from_directory
from http import HTTPStatus
from flask import abort,jsonify
from datetime import datetime




book=Namespace("/",description="end point for Book api")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#book model  marshallow
book_model=book.model(
    "book",{
        "id":fields.Integer(),
        "title":fields.String(),
        "author":fields.String(),
        "description":fields.String(),
        "create":fields.DateTime()
    }
)

#book model  marshallow
framework_model=book.model(
    "Framework",{
        "id":fields.Integer(),
        "name":fields.String(),
        "description":fields.String(),
        "date_creat_at":fields.DateTime()
    }
)
"""
username=db.Column(db.String(50),nullable=False,unique=True)
    email=db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.String(200),nullable=False)
    create_at=db.Column(db.DateTime(),default=datetime.utcnow())
    books = db.relationship('Book',backref='book', lazy=True)
    frameworks =db.relationship('Framework', lazy='select',
        backref=db.backref('framework', lazy='joined'))
    images = db.relationship('UrlPath',backref='image', lazy=True)
    user_model=book.model(
    "UserModel",{
        "id":fields.Integer(),
        "email":fields.String(),
        "password":fields.String(),
        "create_at":fields.DateTime(),
        "books":fields.List([]),
        "frameworks":fields.String(),
        "images":fields.String()
    }
)
class UrlPath(db.Model):
    __tablename__="images"
    id=db.Column(db.Integer(),primary_key=True)
    file_name=db.Column(db.String(100),nullable=False,unique=True)
    url_name=db.Column(db.String(200),nullable=False,)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'),
        nullable=False)

"""
url_model=book.model(
    "UrlPath",{
        "id":fields.Integer(),
        "file_name":fields.String(),
        "url_name":fields.Url("images")
    }
)

user_model=book.model(
    "UserModel",{
        "id":fields.Integer(),
        "email":fields.String(),
        "password":fields.String(),
        "create_at":fields.DateTime(),
        "books":fields.List(fields.Nested(book_model,),),
        "frameworks":fields.List(fields.Nested(framework_model,)),
        "images":fields.List(fields.Nested(url_model))
    })



@book.route("/")
class BooksView(Resource):
    @book.marshal_list_with(book_model,code=200,envelope="books")
    def get(self):
        books=Book.query.all()
        return books

    @book.marshal_with(book_model,code=200)
    def post(self):
        data=request.get_json()
        newbook=Book(
            title=data.get("title"),
            author=data.get("author"),
            description=data.get("description"),
            user_id=data.get("user_id")
        )
        newbook.save()
        return newbook

@book.route("/users",)
class UserView(Resource):
    @book.marshal_list_with(user_model,code=200,envelope="users")
    def get(self):
         user=UserModel.query.all()
         return user
     

@book.route("/users/<int:id>")
class GetUser(Resource):
    @book.marshal_with(user_model,code=200)
    def get(self,id):
        user=UserModel.query.filter_by(id=id).first()
        if user is None:
            abort(401,"user not found")
        return user

@book.route("/images",endpoint='images')
class GetImages(Resource):
    @book.marshal_with(url_model,code=200,envelope="images")
    def get(self):
        images=UrlPath.query.all()
        if images is None:
            abort(401,"images not found")
        return images



@book.route("/<int:id>")
class BookView(Resource):
    @book.marshal_with(book_model)
    def get(self,id):
        book=Book.query.filter_by(id=id).first()
        if book is None:
            return abort(401,"book does not exist")
        return book

    @book.marshal_with(book_model)
    def put(self,id):
        book=Book.query.filter_by(id=id).first()
        if book is None:
            return abort(401,"book does not exist")
        data=request.get_json()
        book.title=data.get("title")
        book.id=data.get("id")
        book.author=data.get("author")
        book.description=data.get("description")
        book.user_id=data.get("user_id")
        book.create=datetime.utcnow()
        book.update()
        return book 

    def delete(self,id):
        book=Book.query.filter_by(id=id).first()
        if book is None:
            return abort(401,"book does not exist")
        book.delete()
        return jsonify(message="book deleted with success")

@book.route("/upload")
class Upload(Resource):
    def post(self):
        if 'file' not in request.files:
            return abort(404,"No file part")
        file=request.files["file"]
        if file.filename == '':
            return abort(401,"no selected file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filter=UrlPath.query.filter_by(file_name=filename).first()
            if filter :
                abort(401,"file already exist")
            url=os.path.join("/Users/aminemejri/Desktop/Apiflask/api/upload", filename)
            filesave=UrlPath(
                file_name=filename,
                url_name=url,
                user_id=1
            )
            filesave.save()
            file.save(os.path.join("/Users/aminemejri/Desktop/Apiflask/api/upload", filename))
        return jsonify(message="file upload witth success",url=url)
    
    
@book.route('/uploads/<filename>')
class Download(Resource):
    def get(self,filename):
        urlimage=UrlPath.query.filter_by(file_name=filename).first()
        if urlimage is None:
            abort(401,f"file not founded")
        return send_from_directory("upload",
                               filename)

