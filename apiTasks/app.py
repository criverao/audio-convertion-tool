from flask_restful import Api
from .modelos import db
from .vistas import VistaSignUp, VistaLogIn, VistaTask, VistaTasks, VistaArchivo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@192.168.1.57:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS']=True
    app.config['UPLOAD_FOLDER']='/home/chgarciaa1/archivos'
    return app

app = create_app('default')
if __name__ == "__main__":
    app.run()
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

