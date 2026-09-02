from sqlalchemy.orm import Session

from models import CalibrationPoint


def linear_fit(db: Session) -> tuple[float | None, float | None, int]:
    points = db.query(CalibrationPoint).all()
    n = len(points)
    if n < 2:
        return None, None, n

    sum_x = sum(p.concentration for p in points)
    sum_y = sum(p.channel_value for p in points)
    sum_xy = sum(p.concentration * p.channel_value for p in points)
    sum_xx = sum(p.concentration * p.concentration for p in points)

    denominator = n * sum_xx - sum_x * sum_x
    if denominator == 0:
        return None, None, n

    m = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - m * sum_x) / n
    return m, b, n


def estimate_concentration(channel_value: float, m: float, b: float) -> float:
    return (channel_value - b) / m
