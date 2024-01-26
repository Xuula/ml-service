import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import joblib

import tables, schemas
from database import SessionLocal, engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, File

from database import get_db

models_router = APIRouter()

    
vectorizer = joblib.load('models/vectorizer.pkl')
MNB = joblib.load('models/MNB.pkl')
SVC = joblib.load('models/SVC.pkl')
models = {'SVC': SVC, 'MNB': MNB}

@models_router.post("/models/process")
def process(file_bytes: bytes = File(), db: Session = Depends(get_db), session_idx: str, model: str):
    global models, vectorizer
    search_res = db.query(tables.Session).filter(tables.Session.idx == session_idx).first()
    if search_res is None:
        resp.status_code = starlette.status.HTTP_400_BAD_REQUEST
        return {"detail": "wrong session identifier"}
    user_id = search_res.user_id
    if not model in modelds:
        resp.status_code = starlette.status.HTTP_400_BAD_REQUEST
        return {"detail": "wrong model name"}
    try:
        data = pd.read_csv(file_bytes)
    except Exception as e:
        resp.status_code = starlette.status.HTTP_400_BAD_REQUEST
        return {"detail": "wrong file format"}
    if not 'Product Title' in data.columns():
        resp.status_code = starlette.status.HTTP_400_BAD_REQUEST
        return {"detail": "csv must contain a column named 'Product Title'"}
    # Проверить монеты на счету
    X = data['Product Title']
    X_v = self._vectorizer.transform(X)
    y = models[model].predict(X_v)
    data['Category ID'] = y

    resFile = tables.File(data=data.to_csv().encode(), name='res.txt', user_idx=user_idx)
    db.add(resFile)
    db.commit()

    return {"status": "ok"}