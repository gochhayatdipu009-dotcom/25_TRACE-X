from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import SessionLocal
from app.utils.logger import logger

from app.osint.username_scanner import scan_username
from app.osint.delta_engine import run_delta_analysis
from app.osint.learning_rules import update_confidence
from app.osint.risk_engine import calculate_platform_risk
from app.osint.reverse_osint_engine import detect_reverse_osint_signals

from app.models.scan_session import ScanSession
from app.models.platform_exposure import PlatformExposure
from app.models.exposure_evidence import ExposureEvidence
from app.models.risk_score import RiskScore

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ScanRequest(BaseModel):
    username: str


@router.post("/scan")
def start_scan(payload: ScanRequest, db: Session = Depends(get_db)):
    username = payload.username.strip()
    logger.info(f"[SCAN] Started scan for username: {username}")

    scan_session = ScanSession(
        input_username=username,
        started_at=datetime.utcnow(),
        scan_version="v1",
    )
    db.add(scan_session)
    db.commit()
    db.refresh(scan_session)

    scan_id = scan_session.id  # ✅ keep as ORM value

    results = scan_username(username)
    platforms_response: list[dict] = []

    for result in results:
        platform = result["platform"]
        status = result["status"]
        exists = status == "confirmed"

        platform_exposure = PlatformExposure(
            scan_session_id=scan_id,
            platform=platform,
            platform_username=username,
            exists=exists,
            status=status,
            first_seen_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow(),
        )

        db.add(platform_exposure)
        db.commit()
        db.refresh(platform_exposure)

        platform_exposure_id = platform_exposure.id  # ✅ DO NOT CAST

        evidence_payload: list[dict] = []

        if exists and result.get("url"):
            evidence = ExposureEvidence(
                platform_exposure_id=platform_exposure_id,
                evidence_type="profile",
                evidence_value=result["url"],
                discovered_at=datetime.utcnow(),
            )
            db.add(evidence)
            db.commit()

            evidence_payload.append({
                "evidence_type": "profile",
                "evidence_value": result["url"],
            })

        run_delta_analysis(
            db=db,
            platform_exposure=platform_exposure,
            current_evidence=evidence_payload,
        )

        update_confidence(db, platform_exposure_id)

        if exists:
            calculate_platform_risk(
                db=db,
                platform_exposure_id=platform_exposure_id,
                platform=platform,
            )

        reverse_flags = detect_reverse_osint_signals(
            db=db,
            platform_exposure_id=platform_exposure_id,
        )

        latest_risk = (
            db.query(RiskScore)
            .filter(
                RiskScore.scope == "platform",
                RiskScore.scope_reference_id == platform_exposure_id,
            )
            .order_by(RiskScore.calculated_at.desc())
            .first()
        )

        platforms_response.append({
            "platform": platform,
            "exists": exists,
            "status": status,
            "url": result.get("url"),
            "evidence_count": len(evidence_payload),
            "risk_score": latest_risk.risk_score if latest_risk else 0,
            "risk_level": latest_risk.risk_level if latest_risk else "Low",
            "reverse_osint_flags": reverse_flags,
        })

    scan_session.completed_at = datetime.utcnow()
    db.commit()

    logger.info(f"[SCAN] Completed scan session {scan_id}")

    return {
        "scan_id": scan_id,
        "username": username,
        "platforms": platforms_response,
    }
