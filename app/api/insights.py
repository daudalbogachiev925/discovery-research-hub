from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import numpy as np
from app.database import get_db
from app.models import Insight
from app.schemas import InsightRead, ClusterSummary
from app.nlp.clusterer import cluster, top_terms

router = APIRouter()

@router.get("", response_model=List[InsightRead])
def list_insights(db: Session = Depends(get_db)):
    return db.query(Insight).all()

@router.post("/recluster")
def recluster(db: Session = Depends(get_db), n_clusters: int = 8):
    rows = db.query(Insight).filter(Insight.embedding.isnot(None)).all()
    if len(rows) < 2:
        return {"clusters": 0}
    vectors = np.array([r.embedding for r in rows])
    labels = cluster(vectors, n_clusters)
    for r, lbl in zip(rows, labels):
        r.cluster_id = int(lbl)
    db.commit()
    return {"clusters": int(len(set(labels)))}

@router.get("/clusters", response_model=List[ClusterSummary])
def clusters(db: Session = Depends(get_db)):
    rows = db.query(Insight).filter(Insight.cluster_id.isnot(None)).all()
    if not rows:
        return []
    by_cluster = {}
    for r in rows:
        by_cluster.setdefault(r.cluster_id, []).append(r.text)
    labels, texts = [], []
    for cid, items in by_cluster.items():
        for t in items:
            labels.append(cid)
            texts.append(t)
    terms = top_terms(texts, labels)
    return [ClusterSummary(cluster_id=cid, size=len(items),
                           top_terms=terms.get(cid, []),
                           sample_text=items[0][:200])
            for cid, items in sorted(by_cluster.items(),
                                      key=lambda x: -len(x[1]))]
