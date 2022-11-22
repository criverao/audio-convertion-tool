from celery import Celery

celery = Celery('tasks', broker = 'redis://192.168.1.57:6379/0')

celery.conf.beat_schedule = {
    "procesar_archivos": {
        "task" : "task.procesar_tareas",
        "schedule": 60.0
    }
}