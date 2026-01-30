# backend/app/osint/learning_rules.py

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.confidence_score import ConfidenceScore
from app.models.delta_event import DeltaEvent
from app.utils.logger import logger


def update_confidence(db: Session, platform_exposure_id: int):
    """
    Update confidence based on recent delta behavior.
    Confidence goes up slowly, down quickly.
    """

    deltas = (
        db.query(DeltaEvent)
        .filter_by(platform_exposure_id=platform_exposure_id)
        .order_by(DeltaEvent.detected_at.desc())
        .limit(5)
        .all()
    )

    if not deltas:
        return

    score = (
        db.query(ConfidenceScore)
        .filter_by(platform_exposure_id=platform_exposure_id)
        .order_by(ConfidenceScore.calculated_at.desc())
        .first()
    )

    current = score.confidence_score if score else 0.3

    # Learning rules
    if any(d.delta_type == "removed" for d in deltas):
        new_score = max(current - 0.2, 0.0)
        reason = "Evidence instability detected"
    elif all(d.delta_type == "new" for d in deltas):
        new_score = min(current + 0.05, 1.0)
        reason = "Persistent new exposure"
    else:
        new_score = current
        reason = "No significant change"

    updated = ConfidenceScore(
        platform_exposure_id=platform_exposure_id,
        confidence_score=new_score,
        confidence_reason=reason,
        calculated_at=datetime.utcnow(),
    )

    db.add(updated)
    db.commit()

    logger.info(
        f"[CONFIDENCE] PlatformExposure {platform_exposure_id} → {new_score:.2f}"
    )
