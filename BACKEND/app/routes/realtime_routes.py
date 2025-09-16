from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import get_db
from ..schemas import RealTimeIn, PriorityIn # type: ignore
from ..services.realtime_service import ingest_realtime # type: ignore
from .. import crud

router = APIRouter(prefix="/realtime", tags=["realtime"])

@router.post("/ingest")
def ingest(rt: RealTimeIn, db: Session = Depends(get_db)):
    try:
        rs = ingest_realtime(db, rt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "ok", "id": rs.id}

@router.post("/priority")
def set_priority(p: PriorityIn, db: Session = Depends(get_db)):
    train = crud.create_train_if_not_exists(db, p.train_number)
    pr = crud.upsert_priority(db, train, p.priority)
    return {"status": "ok", "train_number": train.train_number, "priority": pr.priority}
