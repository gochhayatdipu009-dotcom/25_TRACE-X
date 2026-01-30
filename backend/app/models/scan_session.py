# backend/app/models/scan_session.py

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.base import Base


class ScanSession(Base):
    __tablename__ = "scan_sessions"

    id = Column(Integer, primary_key=True)
    input_username = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    scan_version = Column(String)
