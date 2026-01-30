# app/models/reverse_osint_signal.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.models.base import Base
from datetime import datetime


class ReverseOSINTSignal(Base):
    __tablename__ = "reverse_osint_signals"

    id = Column(Integer, primary_key=True)
    platform_exposure_id = Column(Integer, ForeignKey("platform_exposures.id"))
    signal_type = Column(String)
    explanation = Column(String)
    detected_at = Column(DateTime, default=datetime.utcnow)
