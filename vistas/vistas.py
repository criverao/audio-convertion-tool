from datetime import datetime
from fileinput import filename
import os
from flask import request
from modelos import db,  Usuario, Task, Status
from flask_restful import Resource
from flask import current_app
from google.cloud import storage
from pydub import AudioSegment


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


    audio = AudioSegment.from_file(pathUploaded)
    audio.export(pathProcessed, format=task.newFormat.name)
    subir_archivo(bucket, usuario.nombre, task.fileName.split(".")[0] + "." + task.newFormat.name, pathProcessed)
    task.newFileName = task.fileName.split(".")[0] + "." + task.newFormat.name
    task.status = Status.processed
    db.session.commit()
    #enviar_notificacion(usuario, task.fileName, task.fileName.split(".")[0] + "." + task.newFormat.name)



class VistaTask(Resource):

    def get(self, id_task):
        storage_client = storage.Client.from_service_account_json(current_app.config['KEY_FILE'])
        bucket = storage_client.bucket(current_app.config['BUCKET'])
        tasks = Task.query.filter_by(status='uploaded', id=int(id_task))
        for task in tasks:
            procesar_tarea(bucket, task)
        return {'mensaje':'Tarea procesada exitosamente'}

