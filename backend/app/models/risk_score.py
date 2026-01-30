# backend/app/models/risk_score.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.models.base import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True)

    scope = Column(String)  # platform | aggregated
    scope_reference_id = Column(Integer)

    risk_score = Column(Float)  # 0–100
    risk_level = Column(String)  # Low / Medium / High
    risk_reason = Column(String)

    calculated_at = Column(DateTime, default=datetime.utcnow)
