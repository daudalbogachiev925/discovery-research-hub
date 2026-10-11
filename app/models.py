from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    participant = Column(String, index=True, nullable=False)
    segment = Column(String, index=True)
    role = Column(String)
    transcript = Column(Text, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    insights = relationship("Insight", back_populates="interview",
                            cascade="all, delete-orphan")

class Insight(Base):
    __tablename__ = "insights"
    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    text = Column(Text, nullable=False)
    cluster_id = Column(Integer, index=True)
    sentiment = Column(String)
    embedding = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    interview = relationship("Interview", back_populates="insights")

class JobStory(Base):
    __tablename__ = "job_stories"
    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, index=True)
    situation = Column(String)
    motivation = Column(String)
    outcome = Column(String)
    created_at = Column(DateTime, server_default=func.now())
