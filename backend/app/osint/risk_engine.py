from sqlalchemy.orm import Session
from datetime import datetime

from app.models.platform_exposure import PlatformExposure
from app.models.exposure_evidence import ExposureEvidence
from app.models.delta_event import DeltaEvent
from app.models.risk_score import RiskScore


# -----------------------------
# Utility
# -----------------------------

def clamp(value: float, min_v: float = 0, max_v: float = 100) -> int:
    return int(max(min_v, min(value, max_v)))


def risk_level(score: int) -> str:
    if score < 20:
        return "Low"
    elif score < 50:
        return "Medium"
    else:
        return "High"


# -----------------------------
# Instagram Risk Model
# -----------------------------

def instagram_risk(signals: dict) -> int:
    followers = signals.get("followers", 0)
    following = signals.get("following", 0)
    posts = signals.get("posts", 0)
    verified = signals.get("is_verified_hint", False)

    score = 0

    # Followers = primary exposure
    if followers >= 10_000_000:
        score += 70
    elif followers >= 1_000_000:
        score += 60
    elif followers >= 100_000:
        score += 45
    elif followers >= 10_000:
        score += 30
    elif followers >= 1_000:
        score += 20
    elif followers >= 100:
        score += 10

    # Posting activity
    score += min(posts * 0.15, 15)

    # Influence ratio
    if following > 0:
        ratio = followers / following
        if ratio >= 10:
            score += 10
        elif ratio >= 3:
            score += 5

    # Verified accounts are automatically high-risk
    if verified:
        score += 20

    return clamp(score)


# -----------------------------
# GitHub Risk Model
# -----------------------------

def github_risk(signals: dict) -> int:
    public_repos = signals.get("public_repos", 0)
    followers = signals.get("followers", 0)
    following = signals.get("following", 0)
    stars = signals.get("stars", 0)

    score = 0

    # Public repos = attack surface
    score += min(public_repos * 4, 30)

    # Social exposure
    if followers >= 10_000:
        score += 30
    elif followers >= 1_000:
        score += 20
    elif followers >= 100:
        score += 10

    # Code popularity = blast radius
    score += min(stars * 0.05, 20)

    # Following ratio
    if following > 0:
        ratio = followers / following
        if ratio > 5:
            score += 10

    return clamp(score)


# -----------------------------
# Main Engine
# -----------------------------

def calculate_platform_risk(
    db: Session,
    platform_exposure_id: int,
):
    exposure = db.get(PlatformExposure, platform_exposure_id)

    # HARD FAIL CLOSED
    if not exposure or exposure.status != "confirmed":
        risk_score = 0
        level = "Low"
    else:
        # Get latest evidence
        evidence = (
            db.query(ExposureEvidence)
            .filter(ExposureEvidence.platform_exposure_id == platform_exposure_id)
            .order_by(ExposureEvidence.discovered_at.desc())
            .first()
        )

        signals = evidence.signals if evidence and isinstance(evidence.signals, dict) else {}
        platform = exposure.platform

        if platform == "instagram":
            risk_score = instagram_risk(signals)
        elif platform == "github":
            risk_score = github_risk(signals)
        else:
            risk_score = 0

        # Delta amplification (history-aware)
        delta_count = (
            db.query(DeltaEvent)
            .filter(DeltaEvent.platform_exposure_id == platform_exposure_id)
            .count()
        )

        if delta_count > 0:
            risk_score = clamp(risk_score + min(delta_count * 5, 15))

        level = risk_level(risk_score)

    db.add(
        RiskScore(
            scope="platform",
            scope_reference_id=platform_exposure_id,
            risk_score=risk_score,
            risk_level=level,
            calculated_at=datetime.utcnow(),
        )
    )
    db.commit()
