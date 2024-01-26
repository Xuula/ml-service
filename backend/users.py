import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from database import get_db

users_router = APIRouter()

@users_router.post("/users/", response_model=schemas.PublicUserInfo)
def create_user(user: schemas.Credentials, db: Session = Depends(get_db)):
    db_user = tables.User(name=user.name, email=user.email, password=user.password, coins=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.PublicUserInfo(name=db_user.name, email=db_user.email, idx=db_user.idx, coins=db_user.coins)

@users_router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(tables.User).filter(tables.User.idx == user_id).first()
    return  schemas.PublicUserInfo(name=db_user.name, email=db_user.email, idx=db_user.idx, coins=db_user.coins)