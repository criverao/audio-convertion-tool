from datetime import datetime
from fileinput import filename
import os
from flask import request
from ..modelos import db,  Usuario, UsuarioSchema, Task, TaskSchema, Status, NewFormat
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from celery import Celery
from datetime import datetime
from sqlalchemy import desc
from flask import current_app, send_from_directory
from werkzeug.utils import secure_filename

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='registrar_log')
def registrar_log(*args):
    pass

task_schema = TaskSchema()
usuario_schema = UsuarioSchema()


def crear_carpetas(usuario):
    ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], usuario)
    if not os.path.exists(ruta):
        os.mkdir(ruta)        
        #os.mkdir(usuario.nombre + "/uploaded")        
        #os.mkdir(usuario.nombre + "/processed")
    return ruta


class VistaTasks(Resource):

    
    @jwt_required()
    def post(self):
        usuario=Usuario.query.filter_by(nombre=get_jwt_identity()).first()
        file = request.files['fileName']
        filename = secure_filename(file.filename)
        nueva_task = Task(fileName=file.filename, 
                             newFormat=request.form.get('newFormat') , 
                             status=Status.uploaded, 
                             timeStamp=datetime.now(), usuario=usuario.id)
        db.session.add(nueva_task)
        ruta = crear_carpetas(usuario.nombre)
        file.save(os.path.join(ruta, filename))                
        db.session.commit()
        return task_schema.dump(nueva_task)

    @jwt_required()
    def get(self):
        usuario=Usuario.query.filter_by(nombre=get_jwt_identity()).first()
        max=request.args.get("max", default=99999, type=int)
        order=request.args.get("order", default=0, type=int)
        if order==0:            
            return [task_schema.dump(ta) for ta in Task.query.filter_by(usuario=usuario.id).order_by(Task.id).limit(max)]
        else:
            return [task_schema.dump(ta) for ta in Task.query.filter_by(usuario=usuario.id).order_by(desc(Task.id)).limit(max)]

class VistaTask(Resource):

    @jwt_required()
    def get(self, id_task):
        task=Task.query.get_or_404(id_task)
        return task_schema.dump(task)

    @jwt_required()
    def put(self, id_task):
        task = Task.query.get_or_404(id_task)
        task.newFormat = request.form.get('newFormat')
        task.status = Status.uploaded
        task.newFileName = None
        db.session.commit()
        return task_schema.dump(task)

    @jwt_required()
    def delete(self, id_task):
        task = Task.query.get_or_404(id_task)
        db.session.delete(task)
        db.session.commit()
        return '',204

class VistaArchivo(Resource):
    @jwt_required()
    def get(self, filename):
        uploads = os.path.join(current_app.config['UPLOAD_FOLDER'], get_jwt_identity())
        return send_from_directory(uploads, filename)

class VistaLogIn(Resource):
    def post(self):
            u_nombre = request.json["username"]
            u_contrasena = request.json["password"]
            usuario = Usuario.query.filter_by(nombre=u_nombre, contrasena = u_contrasena).all()
            if usuario:
                token_de_acceso = create_access_token(identity=u_nombre)
                return {'mensaje':'Inicio de sesión exitoso', 'token_de_acceso':token_de_acceso}
            else:
                return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401



class VistaSignUp(Resource):
    
    def post(self):
        if request.json["password1"] != request.json["password2"]:
            return 'El password1 y el password2 deben ser iguales', 501
        nuevo_usuario = Usuario(nombre=request.json["username"], contrasena=request.json["password1"], correo=request.json["email"])
        token_de_acceso = create_access_token(identity=request.json['username'])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'mensaje':'Usuario creado exitosamente', 'token_de_acceso':token_de_acceso}
