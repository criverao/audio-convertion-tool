from datetime import datetime
from fileinput import filename
import os
from flask import request
from modelos import db,  Usuario, UsuarioSchema, Task, TaskSchema, Status, NewFormat
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from celery import Celery
from datetime import datetime
from sqlalchemy import desc
from flask import current_app, send_from_directory
from werkzeug.utils import secure_filename
from google.cloud import storage, pubsub_v1
from concurrent import futures
from collections.abc import Callable
from  google.oauth2 import service_account

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='registrar_log')
def registrar_log(*args):
    pass

task_schema = TaskSchema()
usuario_schema = UsuarioSchema()

def get_callback(publish_future: pubsub_v1.publisher.futures.Future, data: str) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback



def crear_carpetas(usuario):
    ruta = os.path.join(current_app.config['UPLOAD_FOLDER'], usuario)
    if not os.path.exists(ruta):
        os.mkdir(ruta)        
        #os.mkdir(usuario.nombre + "/uploaded")        
        #os.mkdir(usuario.nombre + "/processed")
    return ruta


def upload_blob(file, destination_blob_name, usuario):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client.from_service_account_json(current_app.config['KEY_FILE'])
    bucket = storage_client.bucket(current_app.config['BUCKET'])
    blob = bucket.blob(current_app.config['FOLDER'] + '/' + usuario + '/' + destination_blob_name)
    blob.upload_from_file(file)



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
        #ruta = crear_carpetas(usuario.nombre)
        #file.save(os.path.join(ruta, filename))  
        upload_blob(file, filename, usuario.nombre)
        db.session.commit()

#        os.environ['GOOGLE_APPLICATION_CREDENTIALS']=current_app.config['KEY_FILE']

        cred = service_account.Credentials.from_service_account_file(filename = current_app.config['KEY_FILE']) #or just from_service_account_file('./auth.json')
        publisher = pubsub_v1.PublisherClient(credentials = cred)
        topic_path = publisher.topic_path(current_app.config['PROJECT_ID'], current_app.config['TOPIC_ID'])
        publish_future = publisher.publish(topic_path, str(nueva_task.id).encode("utf-8"))
        publish_futures = []
        # Non-blocking. Publish failures are handled in the callback function.
        publish_future.add_done_callback(get_callback(publish_future, str(nueva_task.id)))
        publish_futures.append(publish_future)
        futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
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
        storage_client = storage.Client.from_service_account_json(current_app.config['KEY_FILE'])
        bucket = storage_client.bucket(current_app.config['BUCKET'])
        blob = bucket.blob(current_app.config['FOLDER'] + '/' + get_jwt_identity() + '/' + filename)
        f = open(os.path.join(current_app.config['TEMP_FOLDER'], filename),'wb')
        blob.download_to_file(f)
        return send_from_directory(current_app.config['TEMP_FOLDER'], filename)

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
