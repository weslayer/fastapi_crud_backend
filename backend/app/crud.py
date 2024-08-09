from sqlalchemy.orm import Session
from . import models, schemas

def get_questions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Question).offset(skip).limit(limit).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(question_text=question.question_text, answer=question.answer)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question
