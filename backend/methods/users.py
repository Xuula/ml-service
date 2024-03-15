import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from database import get_db

from methods.sessions import get_user

users_router = APIRouter()

@users_router.post("/users", response_model=schemas.PublicUserInfo)
def create_user(user: schemas.Credentials, db: Session = Depends(get_db)):
    db_user = tables.User(name=user.name, email=user.email, password=user.password, coins=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.PublicUserInfo(name=db_user.name, email=db_user.email, idx=db_user.idx, coins=db_user.coins)

@users_router.get("/users/{user_id}", response_model=schemas.PublicUserInfo)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(tables.User).filter(tables.User.idx == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"404: User with id {user_id} does not exist.")
    return  schemas.PublicUserInfo(name=db_user.name, email=db_user.email, idx=db_user.idx, coins=db_user.coins)


@users_router.put("/users/coins/{session_idx}", response_model=schemas.PublicUserInfo)
def read_user(session_idx: str, coins_num: int, db: Session = Depends(get_db)):
    user_idx = get_user(db, session_idx)
    if not user_idx:
        raise HTTPException(status_code=401, detail=f"401: Wrong session identifier.")
    db_user = db.query(tables.User).filter(tables.User.idx == user_idx).first()
    db_user.coins += coins_num
    db.commit()
    db.refresh(db_user)
    return  schemas.PublicUserInfo(name=db_user.name, email=db_user.email, idx=db_user.idx, coins=db_user.coins)