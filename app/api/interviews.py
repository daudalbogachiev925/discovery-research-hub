from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Interview, Insight
from app.schemas import InterviewCreate, InterviewRead
from app.nlp.embedder import embed
from app.nlp.extractor import split_insights

router = APIRouter()

@router.post("", response_model=InterviewRead, status_code=201)
def create(payload: InterviewCreate, db: Session = Depends(get_db)):
    interview = Interview(**payload.model_dump())
    db.add(interview)
    db.commit()
    db.refresh(interview)

    texts = split_insights(payload.transcript)
    if texts:
        vectors = embed(texts)
        for text, vec in zip(texts, vectors):
            db.add(Insight(interview_id=interview.id, text=text,
                           embedding=vec.tolist()))
        db.commit()
    return interview

@router.get("", response_model=List[InterviewRead])
def list_all(db: Session = Depends(get_db)):
    return db.query(Interview).all()

@router.get("/{interview_id}", response_model=InterviewRead)
def get_one(interview_id: int, db: Session = Depends(get_db)):
    i = db.query(Interview).get(interview_id)
    if not i:
        raise HTTPException(404, "Interview not found")
    return i

@router.delete("/{interview_id}", status_code=204)
def delete(interview_id: int, db: Session = Depends(get_db)):
    i = db.query(Interview).get(interview_id)
    if not i:
        raise HTTPException(404)
    db.delete(i)
    db.commit()
