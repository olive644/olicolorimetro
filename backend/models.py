from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer

from database import Base


class CalibrationPoint(Base):
    __tablename__ = "calibration_points"

    id = Column(Integer, primary_key=True, index=True)
    concentration = Column(Float, nullable=False)
    r = Column(Float, nullable=False)
    g = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    channel_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    r = Column(Float, nullable=False)
    g = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    channel_value = Column(Float, nullable=False)
    estimated_concentration = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
