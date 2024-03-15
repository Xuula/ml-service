import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
from sqlalchemy.orm import Session
import random
import string

from fastapi import APIRouter, Depends, HTTPException

from database import get_db

s_router = APIRouter()

def new_session_id():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for i in range(30))
    return result_str

def session_exists(db, session):
    return bool(db.query(tables.Session).filter(tables.Session.idx == session).first())

def get_user(db, session):
    item = db.query(tables.Session).filter(tables.Session.idx == session).first()
    if not item:
        return None
    return item.user_idx

@s_router.post("/sessions")
def login(user: schemas.Credentials, db: Session = Depends(get_db)):
    search_res = db.query(tables.User).filter(tables.User.email == user.email).first()
    if search_res is None or user.password != search_res.password:
        raise HTTPException(status_code=401, detail="Wrong email or password")
    
    new_id = new_session_id()
    while session_exists(db, new_id):
        new_id = new_session_id()
    
    session = tables.Session(idx=new_id, user_idx = search_res.idx)
    db.add(session)
    db.commit()
    return schemas.Session(session_idx = new_id, user_idx = search_res.idx)

@s_router.get("/sessions/{session_idx}")
def verifyyy(session_idx: str, db: Session = Depends(get_db)):
    search_res = db.query(tables.Session).filter(tables.Session.idx == session_idx).first()
    if search_res is None:
        raise HTTPException(status_code=401, detail="session identifier is wrong or has expired")
    return schemas.Session(session_idx = search_res.idx, user_idx = search_res.user_idx)