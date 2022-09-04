


import os
import datetime
from venv import create
from xmlrpc.client import DateTime
from flask_restx import Resource,Namespace,fields
from flask import request ,jsonify,Flask
from .models import Book,UrlPath
from werkzeug.utils import secure_filename
from flask import send_from_directory
from http import HTTPStatus
from flask import abort
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
        "user_id":fields.Integer(),
        "create":fields.DateTime()
    }
)

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


