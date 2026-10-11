from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Insight, JobStory
from app.schemas import JobStoryRead
from app.nlp.extractor import to_jtbd

router = APIRouter()

@router.post("/generate")
def generate(db: Session = Depends(get_db)):
    rows = db.query(Insight).filter(Insight.cluster_id.isnot(None)).all()
    by_cluster = {}
    for r in rows:
        by_cluster.setdefault(r.cluster_id, []).append(r.text)

    db.query(JobStory).delete()
    db.commit()
    result = []
    for cid, texts in by_cluster.items():
        js = to_jtbd(texts)
        db.add(JobStory(cluster_id=cid, **js))
        result.append({"cluster_id": cid, **js})
    db.commit()
    return result

@router.get("", response_model=List[JobStoryRead])
def list_stories(db: Session = Depends(get_db)):
    return db.query(JobStory).all()
