from flask_restful import Api
from .modelos import db
from .vistas import VistaSignUp, VistaLogIn, VistaTask, VistaTasks, VistaArchivo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask


def create_app(config_name):
    app = Flask(__name__)  
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:S/K..g?MVGUbg);g@34.132.127.130:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS']=True
    app.config['UPLOAD_FOLDER']='/mnt/archivos'
    app.config['BUCKET']='file-storage-audio'
    app.config['FOLDER']='archivos'
    app.config['TEMP_FOLDER']='/home/cesa96_gmail_com/temp_files'
    app.config['KEY_FILE']='/home/cesa96_gmail_com/key_store/northern-symbol-366812-a5177107a683.json'
    app.config['PROJECT_ID']='northern-symbol-366812'
    app.config['TOPIC_ID']='AudioConverter'
    return app

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaArchivo, '/api/files/<filename>')
jwt = JWTManager(app)

