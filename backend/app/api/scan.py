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
from typing import cast

from app.models.scan_session import ScanSession
from app.models.platform_exposure import PlatformExposure
from app.models.exposure_evidence import ExposureEvidence
from app.models.risk_score import RiskScore

router = APIRouter()


# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Request Schema ----------
class ScanRequest(BaseModel):
    username: str


# ---------- Scan Endpoint ----------
@router.post("/scan")
def start_scan(payload: ScanRequest, db: Session = Depends(get_db)):
    username = payload.username.strip()
    logger.info(f"[SCAN] Started scan for username: {username}")

    # 1️⃣ Create scan session
    scan_session = ScanSession(
        input_username=username,
        started_at=datetime.utcnow(),
        scan_version="v1",
    )
    db.add(scan_session)
    db.commit()
    db.refresh(scan_session)

    scan_id = cast(int, scan_session.id)

    scan_results = scan_username(username)
    platforms_response: list[dict] = []

    # 2️⃣ Process each platform independently
    for result in scan_results:
        platform = result["platform"]
        exists = result["exists"]

        platform_exposure = PlatformExposure(
            scan_session_id=scan_id,
            platform=platform,
            platform_username=username,
            exists=exists,
            first_seen_at=datetime.utcnow(),
            last_seen_at=datetime.utcnow(),
        )
        db.add(platform_exposure)
        db.commit()
        db.refresh(platform_exposure)

        platform_exposure_id = cast(int, platform_exposure.id)
        evidence_payload: list[dict] = []

        # 3️⃣ Evidence
        if exists:
            evidence = ExposureEvidence(
                platform_exposure_id=platform_exposure_id,
                evidence_type="profile",
                evidence_value=result["url"],
                discovered_at=datetime.utcnow(),
            )
            db.add(evidence)
            db.commit()

            evidence_payload.append(
                {
                    "evidence_type": "profile",
                    "evidence_value": result["url"],
                }
            )

        # 4️⃣ Delta analysis
        run_delta_analysis(
            db=db,
            platform_exposure=platform_exposure,
            current_evidence=evidence_payload,
        )

        # 5️⃣ Confidence learning
        #update_confidence(db, platform_exposure_id)

        # 6️⃣ Risk scoring
        calculate_platform_risk(
            db=db,
            platform_exposure_id=platform_exposure_id,
            platform=platform,
        )

        # 7️⃣ Reverse OSINT detection
        reverse_flags = detect_reverse_osint_signals(
            db=db,
            platform_exposure_id=platform_exposure_id,
        ) or []

        latest_risk = (
            db.query(RiskScore)
            .filter(
                RiskScore.scope == "platform",
                RiskScore.scope_reference_id == platform_exposure_id,
            )
            .order_by(RiskScore.calculated_at.desc())
            .first()
        )

        platforms_response.append(
            {
                "platform": platform,
                "exists": exists,
                "evidence_count": len(evidence_payload),
                "risk_score": latest_risk.risk_score if latest_risk else None,
                "risk_level": latest_risk.risk_level if latest_risk else "unknown",
                "reverse_osint_flags": reverse_flags,
            }
        )

    # 8️⃣ Finalize scan session
    setattr(scan_session, "completed_at", datetime.utcnow())
    db.commit()

    logger.info(f"[SCAN] Completed scan session {scan_id}")

    return {
        "scan_id": scan_id,
        "username": username,
        "platforms": platforms_response,
    }
