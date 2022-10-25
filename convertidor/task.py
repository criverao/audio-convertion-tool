from modelos import db, Usuario, Status, Task
from flask.globals import current_app
from celery.signals import task_postrun, worker_process_init
import audiosegment
import os
from flask import Flask
from celery import Celery
import smtplib, ssl
from email.message import EmailMessage


def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['UPLOAD_FOLDER'] = '/home/chgarciaa1/archivos'
    return app


db.app = create_app('default')
db.app_context = db.app.app_context()
db.app_context.push()
db.init_app(db.app)
with db.app.app_context():
    db.create_all()

celery = Celery('tasks', broker='redis://127.0.0.1:6379/0')


def crear_carpetas(usuario):
    ruta = os.path.join(db.app.config['UPLOAD_FOLDER'], usuario.nombre)
    if not os.path.exists(ruta):
        os.mkdir(ruta)
        # os.mkdir(usuario.nombre + "/uploaded")
        # os.mkdir(usuario.nombre + "/processed")
    return ruta


def procesar_tarea(task):
    usuario = Usuario.query.get(task.usuario)
    carpetaUsuario = crear_carpetas(usuario)

    pathUploaded = os.path.join(carpetaUsuario, task.fileName)
    pathProcessed = os.path.join(carpetaUsuario, task.fileName.split(".")[0] + "." + task.newFormat.name)

    audio = audiosegment.from_file(pathUploaded)
    audio.export(pathProcessed, format=task.newFormat.name)

    task.newFileName = task.fileName.split(".")[0] + "." + task.newFormat.name
    task.status = Status.processed
    db.session.commit()
    enviar_notificacion(usuario, task.fileName, task.fileName.split(".")[0] + "." + task.newFormat.name)


@celery.task
def procesar_tareas():
    tasks = Task.query.filter_by(status='uploaded')
    for task in tasks:
        procesar_tarea(task)


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
    msg.set_content('El nuevo archivo {} ya se encuentra disponible '.format(archivoDestino))

    msg['Subject'] = 'Notificacion transformacion del archivo {}'.format(archivoOrigen)
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

