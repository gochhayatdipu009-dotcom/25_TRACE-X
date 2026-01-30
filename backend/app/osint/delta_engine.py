from datetime import datetime
from sqlalchemy.orm import Session

from app.models.delta_event import DeltaEvent
from app.models.exposure_evidence import ExposureEvidence


def run_delta_analysis(
    db: Session,
    platform_exposure,
    current_evidence: list[dict],
):
    
    previous = (
        db.query(ExposureEvidence)
        .filter(
            ExposureEvidence.platform_exposure_id == platform_exposure.id
        )
        .order_by(ExposureEvidence.discovered_at.desc())
        .first()
    )

    
    if not previous:
        return

    previous_value = previous.evidence_value
    current_value = current_evidence[0]["evidence_value"] if current_evidence else None

    
    if previous_value == current_value:
        return

    delta = DeltaEvent(
        platform_exposure_id=platform_exposure.id,
        delta_type="changed",
        previous_value=previous_value,
        current_value=current_value,
        detected_at=datetime.utcnow(),
    )

    db.add(delta)
    db.commit()
