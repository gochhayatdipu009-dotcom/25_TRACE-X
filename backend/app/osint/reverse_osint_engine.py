# backend/app/osint/reverse_osint_engine.py

from sqlalchemy.orm import Session
from app.models.delta_event import DeltaEvent


def detect_reverse_osint_signals(
    db: Session,
    platform_exposure_id: int,
) -> list[dict]:
    """
    Detect reverse-OSINT patterns from recent delta events.
    SAFE for Pylance + SQLAlchemy.
    """

    # ✅ Query returns Python objects (NOT expressions)
    events: list[DeltaEvent] = (
        db.query(DeltaEvent)
        .filter(DeltaEvent.platform_exposure_id == platform_exposure_id)
        .order_by(DeltaEvent.detected_at.desc())
        .limit(10)
        .all()
    )

    if not events:
        return []

    # ✅ ONLY Python attribute access below
    new_events = []
    removed_events = []

    for e in events:
        if e.delta_type == "new":
            new_events.append(e)
        elif e.delta_type == "removed":
            removed_events.append(e)

    flags: list[dict] = []

    # Heuristic 1: Reappearing profile
    if len(new_events) >= 3:
        flags.append(
            {
                "signal": "reappearing_profile",
                "explanation": (
                    "Profile appeared multiple times after disappearance. "
                    "This may indicate burner or controlled identity reuse."
                ),
                "confidence": "medium",
            }
        )

    # Heuristic 2: Profile wipe
    if len(removed_events) >= 3:
        flags.append(
            {
                "signal": "profile_wipe",
                "explanation": (
                    "Multiple profile elements were removed in a short time. "
                    "This may indicate an intentional cleanup."
                ),
                "confidence": "medium",
            }
        )

    return flags
