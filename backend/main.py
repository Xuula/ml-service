from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

from methods.users import users_router
from methods.sessions import s_router
from methods.documents import docs_router
from methods.tasks import tasks_router

import tables
from database import engine

tables.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(users_router)
app.include_router(s_router)
app.include_router(docs_router)
app.include_router(tasks_router)

