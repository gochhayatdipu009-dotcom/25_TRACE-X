from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.delta_event import DeltaEvent
from app.models.platform_exposure import PlatformExposure

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/scan/{scan_id}/timeline")
def get_timeline(scan_id: int, db: Session = Depends(get_db)):
    events = (
        db.query(DeltaEvent)
        .join(
            PlatformExposure,
            DeltaEvent.platform_exposure_id == PlatformExposure.id
        )
        .filter(PlatformExposure.scan_session_id == scan_id)
        .order_by(DeltaEvent.detected_at.desc())
        .all()
    )

    return [
        {
            # 🔴 FIX IS HERE
            "event_type": e.delta_type,   # ← was e.event_type (wrong)
            "platform_exposure_id": e.platform_exposure_id,
            "previous_value": e.previous_value,
            "current_value": e.current_value,
            "detected_at": e.detected_at.isoformat(),
        }
        for e in events
    ]
