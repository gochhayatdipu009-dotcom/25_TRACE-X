# backend/app/osint/delta_engine.py

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.platform_exposure import PlatformExposure
from app.models.exposure_evidence import ExposureEvidence
from app.models.delta_event import DeltaEvent
from app.utils.logger import logger


def run_delta_analysis(
    db: Session,
    platform_exposure: PlatformExposure,
    current_evidence: list[dict],
):
    """
    DEV MODE:
    Always emit a delta event so timeline is visible.
    This proves the pipeline works.
    """

    # 🔴 FORCE a delta event on every scan (DEV ONLY)
    delta = DeltaEvent(
        platform_exposure_id=platform_exposure.id,
        delta_type="new",
        previous_value=None,
        current_value="forced_dev_delta",
        detected_at=datetime.utcnow(),
    )

    db.add(delta)
    db.commit()

    logger.info(
        f"[DELTA][DEV] Forced delta event for platform "
        f"{platform_exposure.platform}"
    )
