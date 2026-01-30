# backend/app/models/exposure_evidence.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base


class ExposureEvidence(Base):
    __tablename__ = "exposure_evidence"

    id = Column(Integer, primary_key=True)
    platform_exposure_id = Column(Integer, ForeignKey("platform_exposures.id"))

    evidence_type = Column(String)   # profile, repo, post, metadata, mention
    evidence_value = Column(String)  # URL / hash / identifier

    discovered_at = Column(DateTime, default=datetime.utcnow)
