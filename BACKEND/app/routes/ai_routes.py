from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app import get_db
from ..services.static_schedule import import_schedule_csv
from .. import schemas

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.post("/upload_csv", response_model=schemas.UploadScheduleResult)
async def upload_schedule(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        rows, created_trains, created_stations = import_schedule_csv(db, content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"rows": rows, "created_trains": created_trains, "created_stations": created_stations}
