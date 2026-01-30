from app.db.session import engine
from app.models.base import Base

# 🔥 FORCE model registration (THIS IS THE MISSING PIECE)
from app.models.scan_session import ScanSession
from app.models.platform_exposure import PlatformExposure
from app.models.exposure_evidence import ExposureEvidence
from app.models.delta_event import DeltaEvent
from app.models.risk_score import RiskScore
from app.models.confidence_score import ConfidenceScore


def init_db():
    Base.metadata.create_all(bind=engine)
    print("DB initialized successfully")


if __name__ == "__main__":
    init_db()
