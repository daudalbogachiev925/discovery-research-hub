from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class InterviewCreate(BaseModel):
    participant: str
    segment: Optional[str] = None
    role: Optional[str] = None
    transcript: str
    notes: Optional[str] = None

class InterviewRead(InterviewCreate):
    id: int
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

class InsightRead(BaseModel):
    id: int
    interview_id: int
    text: str
    cluster_id: Optional[int]
    sentiment: Optional[str]
    class Config:
        from_attributes = True

class ClusterSummary(BaseModel):
    cluster_id: int
    size: int
    top_terms: List[str]
    sample_text: str

class JobStoryRead(BaseModel):
    id: int
    cluster_id: int
    situation: str
    motivation: str
    outcome: str
    class Config:
        from_attributes = True
