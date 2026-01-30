# backend/app/models/platform_exposure.py

from sqlalchemy import (
    Column, Integer, String, Boolean,
    DateTime, ForeignKey, UniqueConstraint
)
from datetime import datetime
from app.models.base import Base


class PlatformExposure(Base):
    __tablename__ = "platform_exposures"

    id = Column(Integer, primary_key=True)
    scan_session_id = Column(Integer, ForeignKey("scan_sessions.id"))

    platform = Column(String, index=True)
    platform_username = Column(String)

    exists = Column(Boolean, default=False)

    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("scan_session_id", "platform"),
    )
