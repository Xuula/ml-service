import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
from sqlalchemy.orm import Session


from fastapi import APIRouter, Depends, HTTPException

from database import get_db

from methods.sessions import get_user

tasks_router = APIRouter()

@tasks_router.get("/tasks/get/{task_idx}", response_model=schemas.Task)
def read_user(task_idx: int, session_idx: str, db: Session = Depends(get_db)):
    user = get_user(db, session_idx)
    if not user:
        raise HTTPException(status_code=401, detail=f"401: Session expired")
    db_task = db.query(tables.Task).filter(tables.Task.idx == task_idx).first()
    if not db_task:
        raise HTTPException(status_code=404, detail=f"404: Task with id {task_idx} does not exist.")
    if db_task.owner_idx != user:
        print(db_task.owner_idx,  user)
        raise HTTPException(status_code=401, detail="User does not have access to this task or session identifier is incorrect or has expired.")
    return schemas.Task(idx=db_task.idx, status=db_task.status, document_idx=db_task.file_idx, result_idx=db_task.result_idx,
                        error=db_task.error)

@tasks_router.get("/tasks/getall/{session_idx}")
def read_user(session_idx: str, db: Session = Depends(get_db)):
    user = get_user(db, session_idx)
    if not user:
        raise HTTPException(status_code=401, detail=f"401: Session expired")
    tasks = db.query(tables.Task).filter(tables.Task.owner_idx == user).all()
    res = []
    for task in tasks:
        file_idx = task.file_idx
        db_file = tasks = db.query(tables.File).filter(tables.File.idx == file_idx).first()
        filename = db_file.name
        res.append({'idx': task.idx, 'status': task.status, 'error': task.error, 'file': filename})
    return {'tasks': res}