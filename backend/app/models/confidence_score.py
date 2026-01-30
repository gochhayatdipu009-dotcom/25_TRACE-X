# backend/app/models/confidence_score.py

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base


class ConfidenceScore(Base):
    __tablename__ = "confidence_scores"

    id = Column(Integer, primary_key=True)
    platform_exposure_id = Column(Integer, ForeignKey("platform_exposures.id"))

    confidence_score = Column(Float)  # 0.0 – 1.0
    confidence_reason = Column(String)

    calculated_at = Column(DateTime, default=datetime.utcnow)
