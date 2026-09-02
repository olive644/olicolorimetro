from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import calibration
import models
import schemas
import vision
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Colorimetro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/calibration-points", response_model=schemas.CalibrationPointOut)
async def create_calibration_point(
    concentration: float = Form(...),
    roi_x: float = Form(...),
    roi_y: float = Form(...),
    roi_w: float = Form(...),
    roi_h: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    raw_bytes = await image.read()
    try:
        result = vision.analyze(raw_bytes, roi_x, roi_y, roi_w, roi_h)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    point = models.CalibrationPoint(
        concentration=concentration,
        r=result["r"],
        g=result["g"],
        b=result["b"],
        channel_value=result["channel_value"],
    )
    db.add(point)
    db.commit()
    db.refresh(point)
    return point


@app.get("/api/calibration-points", response_model=list[schemas.CalibrationPointOut])
def list_calibration_points(db: Session = Depends(get_db)):
    return db.query(models.CalibrationPoint).order_by(models.CalibrationPoint.concentration).all()


@app.delete("/api/calibration-points/{point_id}")
def delete_calibration_point(point_id: int, db: Session = Depends(get_db)):
    point = db.get(models.CalibrationPoint, point_id)
    if point is None:
        raise HTTPException(status_code=404, detail="Ponto de calibração não encontrado.")
    db.delete(point)
    db.commit()
    return {"deleted": point_id}


@app.get("/api/fit", response_model=schemas.FitOut)
def get_fit(db: Session = Depends(get_db)):
    m, b, n = calibration.linear_fit(db)
    return schemas.FitOut(m=m, b=b, points_used=n)


@app.post("/api/readings", response_model=schemas.ReadingOut)
async def create_reading(
    roi_x: float = Form(...),
    roi_y: float = Form(...),
    roi_w: float = Form(...),
    roi_h: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    raw_bytes = await image.read()
    try:
        result = vision.analyze(raw_bytes, roi_x, roi_y, roi_w, roi_h)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    m, b, _ = calibration.linear_fit(db)
    estimated = calibration.estimate_concentration(result["channel_value"], m, b) if m else None

    reading = models.Reading(
        r=result["r"],
        g=result["g"],
        b=result["b"],
        channel_value=result["channel_value"],
        estimated_concentration=estimated,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@app.get("/api/readings", response_model=list[schemas.ReadingOut])
def list_readings(db: Session = Depends(get_db)):
    return db.query(models.Reading).order_by(models.Reading.created_at.desc()).limit(50).all()
