import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
import starlette
from starlette.responses import Response
from sqlalchemy.orm import Session
import random
import string

from fastapi import APIRouter, Depends

from database import get_db

s_router = APIRouter()

def new_session_id():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for i in range(30))
    return result_str

def session_exists(db, session):
    return bool(db.query(tables.Session).filter(tables.Session.idx == session).first())

@s_router.post("/sessions")
def login(user: schemas.Credentials, resp: Response, db: Session = Depends(get_db)):
    search_res = db.query(tables.User).filter(tables.User.email == user.email).first()
    if search_res is None or user.password != search_res.password:
        resp.status_code = starlette.status.HTTP_400_BAD_REQUEST
        return {"detail": "wrong email or password"}
    
    new_id = new_session_id()
    while session_exists(db, new_id):
        new_id = new_session_id()
    
    session = tables.Session(idx=new_id, user_idx = search_res.idx)
    db.add(session)
    db.commit()
    return schemas.Session(session_idx = new_id)

@s_router.get("/sessions/verify")
def verify(session_idx: str, db: Session = Depends(get_db)):
    search_res = db.query(tables.Session).filter(tables.Session.idx == session_idx).first()
    if search_res is None:
        return {'status': 'WRONG_IDENTIFYER'}
    return {'status': 'CORRECT_IDENTIFYER', 'user_idx': search_res.user_idx}