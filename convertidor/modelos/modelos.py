from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

class Status(enum.Enum):
   uploaded = 1
   processed = 2

class NewFormat(enum.Enum):
   wav = 1
   mp3 = 2
   aac = 3
   ogg = 4
   xwma = 5

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)    
    fileName = db.Column(db.String(128))
    newFormat = db.Column(db.Enum(NewFormat))
    status = db.Column(db.Enum(Status))
    timeStamp = db.Column(db.DateTime(10))
    newFileName = db.Column(db.String(128))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    correo = db.Column(db.String(128))
    tasks = db.relationship('Task', cascade='all, delete, delete-orphan')
    
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}    

class TaskSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=("status"))
    newFormat = EnumADiccionario(attribute=("newFormat"))
    class Meta:
         model = Task
         include_relationships = True
         load_instance = True
         
class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = False
         load_instance = True         
         
