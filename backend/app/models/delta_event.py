from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base


class DeltaEvent(Base):
    __tablename__ = "delta_events"

    id = Column(Integer, primary_key=True, index=True)
    platform_exposure_id = Column(
        Integer,
        ForeignKey("platform_exposures.id"),
        nullable=False,
        index=True,
    )

    # 🔑 THIS IS THE FIELD USED EVERYWHERE
    delta_type = Column(String, nullable=False)  # new | removed | changed

    previous_value = Column(String, nullable=True)
    current_value = Column(String, nullable=True)

    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
