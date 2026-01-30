from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base


class PlatformExposure(Base):
    __tablename__ = "platform_exposures"

    id = Column(Integer, primary_key=True)

    scan_session_id = Column(Integer, ForeignKey("scan_sessions.id"), nullable=False)

    platform = Column(String, nullable=False)
    platform_username = Column(String, nullable=False)

    exists = Column(Boolean, default=False)
    status = Column(String, nullable=False)  # confirmed | not_found | blocked | error

    first_seen_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
