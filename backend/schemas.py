from datetime import datetime

from pydantic import BaseModel


class CalibrationPointOut(BaseModel):
    id: int
    concentration: float
    r: float
    g: float
    b: float
    channel_value: float
    created_at: datetime

    class Config:
        from_attributes = True


class ReadingOut(BaseModel):
    id: int
    r: float
    g: float
    b: float
    channel_value: float
    estimated_concentration: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class FitOut(BaseModel):
    m: float | None
    b: float | None
    points_used: int
