from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)

@app.get("/questions/", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    questions = crud.get_questions(db, skip=skip, limit=limit)
    return questions
