"""
AgroScan AI – SQLAlchemy ORM Models
=====================================
Defines all database tables. Tables are auto-created by init_db() on startup.
"""

from sqlalchemy import (
    Column, String, Float, Boolean, DateTime, Integer,
    Text, ARRAY, func
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from database import Base
import uuid


class ScanResult(Base):
    """Stores every crop disease scan prediction."""
    __tablename__ = "scan_results"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    scan_id    = Column(String(8),  unique=True, nullable=False, index=True,
                        default=lambda: str(uuid.uuid4())[:8])
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # --- Input ---
    crop       = Column(String(50),  nullable=False, index=True)
    filename   = Column(String(255), nullable=True)
    file_size_kb = Column(Float,     nullable=True)

    # --- Prediction output ---
    disease_name    = Column(String(120), nullable=False)
    scientific_name = Column(String(120), nullable=True)
    icon            = Column(String(10),  nullable=True)
    confidence      = Column(Float,       nullable=False)
    severity        = Column(String(20),  nullable=False)   # high | moderate | none
    is_healthy      = Column(Boolean,     nullable=False, default=False)

    # --- Rich detail (stored as JSONB for flexibility) ---
    cause            = Column(Text,  nullable=True)
    urgency          = Column(Text,  nullable=True)
    symptoms         = Column(JSONB, nullable=True)   # list[str]
    treatment        = Column(JSONB, nullable=True)   # list[str]
    prevention       = Column(JSONB, nullable=True)   # list[str]
    affected_regions = Column(JSONB, nullable=True)   # list[str]

    def to_dict(self) -> dict:
        """Serialize the row back to the same JSON shape the frontend expects."""
        return {
            "scan_id":          self.scan_id,
            "timestamp":        self.created_at.isoformat() if self.created_at else None,
            "crop":             self.crop,
            "filename":         self.filename,
            "file_size_kb":     self.file_size_kb,
            "disease_name":     self.disease_name,
            "scientific_name":  self.scientific_name,
            "icon":             self.icon,
            "confidence":       self.confidence,
            "severity":         self.severity,
            "is_healthy":       self.is_healthy,
            "cause":            self.cause,
            "urgency":          self.urgency,
            "symptoms":         self.symptoms or [],
            "treatment":        self.treatment or [],
            "prevention":       self.prevention or [],
            "affected_regions": self.affected_regions or [],
        }
