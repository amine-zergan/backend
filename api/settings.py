import os


baseDir = os.path.dirname(os.path.realpath(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    


class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(baseDir,"book.sqlite3")
    SECRET_KEY="hnhbnhewiwiyiwew"
    UPLOAD_FOLDER="/Users/aminemejri/Desktop/Apiflask/api/upload"
    MAX_CONTENT_LENGTH=16 * 1000 * 1000



class ProdConfig(Config):
    DEBUG=False
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY=os.getenv("SECRET_KEY")
    MAX_CONTENT_LENGTH=16 * 1000 * 1000


config_dict={
    "dev":DevConfig,
    "prod":ProdConfig,
}