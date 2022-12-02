from modelos import db
#import audiosegment
from flask import Flask, render_template
from flask_restful import Api
from vistas import VistaTask
from flask_cors import CORS

def create_app(config_name):
    app = Flask(__name__)    
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:S/K..g?MVGUbg);g@34.132.127.130:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS']=True
    app.config['UPLOAD_FOLDER']='/mnt/archivos'
    app.config['BUCKET']='file-storage-audio'
    app.config['FOLDER']='archivos'
    app.config['TEMP_FOLDER']='/tmp'
    app.config['KEY_FILE']='key_store/northern-symbol-366812-a5177107a683.json'
    app.config['PROJECT_ID']='northern-symbol-366812'
    app.config['TOPIC_ID']='AudioConverter'
    app.config['SUBSCRIPTION_ID']='AudioConverter-sub'
    return app


app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
