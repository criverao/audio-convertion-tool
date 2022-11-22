from modelos import db, Usuario, Status, Task
from flask.globals import current_app
from celery.signals import task_postrun, worker_process_init
import audiosegment
import os
from flask import Flask
from celery import  Celery
import smtplib, ssl
from email.message import EmailMessage
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import pubsub_v1
import logging
from concurrent import futures



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
    app.config['SUBSCRIPTION_ID']='AudioConverter-sub'
    return app



db.app = create_app('default')
db.app_context = db.app.app_context()
db.app_context.push()
db.init_app(db.app)
with db.app.app_context():
    db.create_all()


cred = service_account.Credentials.from_service_account_file(current_app.config['KEY_FILE']) #or just from_service_account_file('./auth.json')
subscriber = pubsub_v1.SubscriberClient(credentials = cred)
subscription_path = subscriber.subscription_path(current_app.config['PROJECT_ID'], current_app.config['SUBSCRIPTION_ID'])

celery = Celery('tasks', broker = 'redis://127.0.0.1:6379/0')


def callback(message):
    with db.app.app_context():
        print('se procesa el mensaje' + message.data.decode('utf-8'))
        storage_client = storage.Client.from_service_account_json(current_app.config['KEY_FILE'])
        bucket = storage_client.bucket(current_app.config['BUCKET'])
        tasks = Task.query.filter_by(status='uploaded', id=int(message.data))
        for task in tasks:
            procesar_tarea(bucket, task)
        message.ack()



def crear_carpetas(usuario):
    ruta = os.path.join(db.app.config['UPLOAD_FOLDER'], usuario.nombre)
    if not os.path.exists(ruta):
        os.mkdir(ruta)        
        #os.mkdir(usuario.nombre + "/uploaded")        
        #os.mkdir(usuario.nombre + "/processed")
    return ruta

def descargar_archivos(bucket, usuario, filename):
    blob = bucket.blob(current_app.config['FOLDER'] + '/' + usuario + '/' + filename)
    f = open(os.path.join(current_app.config['TEMP_FOLDER'], filename),'wb')
    blob.download_to_file(f)

def subir_archivo(bucket, usuario, filename, pathTemp):
    blob = bucket.blob(current_app.config['FOLDER'] + '/' + usuario + '/' + filename)
#    f = open(os.path.join(current_app.config['TEMP_FOLDER'], filename),'r')
    blob.upload_from_filename(pathTemp)

def procesar_tarea(bucket, task):
    usuario = Usuario.query.get(task.usuario)
    descargar_archivos(bucket, usuario.nombre, task.fileName)
    
    pathUploaded = os.path.join(current_app.config['TEMP_FOLDER'], task.fileName)
    pathProcessed = os.path.join(current_app.config['TEMP_FOLDER'], task.fileName.split(".")[0] + "." + task.newFormat.name)

    audio = audiosegment.from_file(pathUploaded)
    audio.export(pathProcessed, format=task.newFormat.name)
    subir_archivo(bucket, usuario.nombre, task.fileName.split(".")[0] + "." + task.newFormat.name, pathProcessed)
    task.newFileName = task.fileName.split(".")[0] + "." + task.newFormat.name
    task.status = Status.processed
    db.session.commit()
    #enviar_notificacion(usuario, task.fileName, task.fileName.split(".")[0] + "." + task.newFormat.name)
    
@celery.task
def procesar_tareas():
    future = subscriber.subscribe(subscription_path, callback=callback)
    with subscriber:
        try:
            future.result(timeout=100)
        except futures.TimeoutError:
            future.cancel()  # Trigger the shutdown.
            future.result()  # Block until the shutdown is complete.

        
@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()        

def enviar_notificacion(usuario, archivoOrigen, archivoDestino):
    port = 465  # For SSL
    smtp_server = "mail.cirkus.com.co"
    sender_email = "cesar.garcia@cirkus.com.co"  # Enter your address
    receiver_email = usuario.correo  # Enter receiver address
    password = "c3s4r10n"
    msg = EmailMessage()
    msg.set_content('El nuevo archivo {} ya se encuentra disponible '.format( archivoDestino))

    msg['Subject'] = 'Notificacion transformacion del archivo {}'.format(archivoOrigen)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)
