# backend/app/osint/risk_engine.py

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.risk_score import RiskScore
from app.models.platform_exposure import PlatformExposure
from app.utils.logger import logger


def _normalize_risk_level(score: float) -> str:
    """
    Convert numeric risk score into categorical level.
    Single source of truth.
    """
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"


def calculate_platform_risk(
    db: Session,
    platform_exposure_id: int,
    platform: str,
) -> None:
    """
    Calculates and stores platform risk score + normalized risk level.
    """

    # 🔹 Basic weighted scoring (can evolve later)
    exposure_weight = {
        "github": 15,
        "twitter": 20,
        "instagram": 25,
    }.get(platform.lower(), 10)

    # 🔹 Growth factor (future delta-based logic hook)
    growth_factor = 1.0

    raw_score = exposure_weight * growth_factor
    risk_score = round(min(raw_score, 100.0), 2)

    risk_level = _normalize_risk_level(risk_score)

    risk = RiskScore(
        scope="platform",
        scope_reference_id=platform_exposure_id,
        risk_score=risk_score,
        risk_level=risk_level,
        calculated_at=datetime.utcnow(),
    )

    db.add(risk)
    db.commit()

    logger.info(
        f"[RISK] PlatformExposure {platform_exposure_id} "
        f"→ score={risk_score} level={risk_level}"
    )
