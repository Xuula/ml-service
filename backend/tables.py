from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    idx = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, index=True)
    coins = Column(Integer)

class Session(Base):
    __tablename__ = "sessions"

    idx = Column(String, index=True, primary_key=True)
    user_idx = Column(String, ForeignKey("users.idx"))
    expires_at = Column(DateTime)


class File(Base):
    __tablename__ = "files"

    idx = Column(Integer, index=True, primary_key=True)
    data = Column(LargeBinary)
    name = Column(String)
    user_idx = Column(String, ForeignKey("users.idx"))
    expires_at = Column(DateTime)

