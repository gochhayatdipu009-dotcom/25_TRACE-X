from sqlalchemy.orm import Session
from app.models.exposure_evidence import ExposureEvidence
from app.models.delta_event import DeltaEvent
from app.models.risk_score import RiskScore
from datetime import datetime

BASE_PLATFORM_RISK = {
    "github": 10,
    "twitter": 15,
    "instagram": 20,
}


def calculate_platform_risk(
    db: Session,
    platform_exposure_id: int,
    platform: str,
):
    base = BASE_PLATFORM_RISK.get(platform, 5)

    evidence_count = db.query(ExposureEvidence)\
        .filter_by(platform_exposure_id=platform_exposure_id)\
        .count()

    delta_count = db.query(DeltaEvent)\
        .filter_by(platform_exposure_id=platform_exposure_id)\
        .count()

    risk_score = base + (evidence_count * 5) + (delta_count * 10)
    risk_score = min(risk_score, 100)

    if risk_score <= 20:
        level = "Low"
    elif risk_score <= 50:
        level = "Medium"
    else:
        level = "High"

    risk = RiskScore(
        scope="platform",
        scope_reference_id=platform_exposure_id,
        risk_score=risk_score,
        risk_level=level,
        calculated_at=datetime.utcnow(),
    )

    db.add(risk)
    db.commit()
