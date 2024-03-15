from celery import Celery

from models import models
from database import SessionLocal
import tables

celery_app = Celery('file_processing', broker='pyamqp://guest@localhost//')

def create_document(db, binary, user_idx, name):
    db_file = tables.File(name= name, data=binary, user_idx = user_idx)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.idx

@celery_app.task(name='process-file')
def process_file(task_idx, file_idx, model):
    db = SessionLocal()
    db_task = db.query(tables.Task).filter(tables.Task.idx == task_idx).first()
    db_task.status = 'Processing'
    db.commit()

    db_file = db.query(tables.File).filter(tables.File.idx == file_idx).first()

    document = models.create_document(db_file.data)
    if not document.load():
        db_task.status = 'Error'
        db_task.error = "Документ не подходит - скорее всего, он не формата csv."
        db.commit()
        return

    user_idx = db_file.user_idx
    db_user = db.query(tables.User).filter(tables.User.idx == user_idx).first()
    coins = db_user.coins
    if coins < 150:
        db_task.status = 'Error'
        db_task.error = "Не хватает токенов на счету"
        db.commit()
        return
    
    db_user.coins -= 150
    db.commit()

    result_data = document.process(model)

    result_name = db_file.name + ' - processed'
    idx = create_document(db, result_data, user_idx, result_name)

    db_task.status = 'Complete'
    db_task.result_idx = idx
    db.commit()


if __name__ == '__main__':
    #celery.worker_main(['worker', '--loglevel=info', '--include=file_processing'])
    celery_app.worker_main(['worker', '--loglevel=info'])