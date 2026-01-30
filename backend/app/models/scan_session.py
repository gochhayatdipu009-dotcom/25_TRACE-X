from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base


class ScanSession(Base):
    __tablename__ = "scan_sessions"

    id = Column(Integer, primary_key=True, index=True)
    input_username = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    scan_version = Column(String, nullable=False)
