import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import Response, StreamingResponse
from io import BytesIO
from email.header import Header

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from database import get_db, SessionLocal
from methods import sessions
from models import models
from file_processing import process_file

docs_router = APIRouter()

def create_document(db, binary, user_idx, name):
    db_file = tables.File(name= name, data=binary, user_idx = user_idx)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file.idx

@docs_router.post("/documents/upload/{session_idx}", response_model=schemas.Document)
async def upload_file(session_idx: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user = sessions.get_user(db, session_idx)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong session identifier")
    file_content = await file.read()
    idx = create_document(db, file_content, user, file.filename)
    return schemas.Document(idx=idx)

def check_for_access_errors(db, file_idx, session_idx):
    user = sessions.get_user(db, session_idx)
    if not user:
        raise HTTPException(status_code=401, detail="Wrong session identifier")
    file = db.query(tables.File).filter(tables.File.idx == file_idx).first()
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    if file.user_idx != user:
        raise HTTPException(status_code=401, detail="This user does not have access to this file.")
    return None

@docs_router.get("/documents/getall/{session_idx}")
async def get_all(session_idx: str, db: Session = Depends(get_db)):
    user_idx = sessions.get_user(db, session_idx)
    if not user_idx:
        raise HTTPException(status_code=401, detail="Wrong session identifier")

    files = db.query(tables.File).filter(tables.File.user_idx == user_idx).all()
    resp = [{'idx': file.idx, 'name': file.name} for file in files]
    return {'files': resp}


@docs_router.get("/documents/download/{file_idx}")
async def download_file(file_idx: int, session_idx: str, db: Session = Depends(get_db)):
    error = check_for_access_errors(db, file_idx, session_idx)
    if error != None:
        return error

    file = db.query(tables.File).filter(tables.File.idx == file_idx).first()
    filename = Header(file.name, 'utf-8').encode()
    return StreamingResponse(BytesIO(file.data), media_type="application/octet-stream", headers={
        'Content-Disposition': f'attachment; filename={filename}'})


@docs_router.post('/documents/process/{file_idx}', response_model=schemas.Task)
async def process(file_idx: int, model: str, session_idx: str, db: Session = Depends(get_db)):
    check_for_access_errors(db, file_idx, session_idx)
    user = sessions.get_user(db, session_idx)

    if not models.is_correct_model(model):
        raise HTTPException(status_code=400, detail="Wrong model name")
    
    coins = db.query(tables.User).filter(tables.User.idx == user).first().coins
    if coins < 150:
        raise HTTPException(status_code=400, detail="Not enough tokens")
    
    db_task = tables.Task(file_idx=file_idx, status="In queue", owner_idx=user)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    process_file.delay(db_task.idx, file_idx, model)

    return schemas.Task(idx=db_task.idx, status=db_task.status, document_idx=db_task.file_idx, result_idx=db_task.result_idx,
                        error=db_task.error)
