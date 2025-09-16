from sqlalchemy.orm import Session
from .. import crud
from ..schemas import RealTimeIn # type: ignore
from typing import Optional

def ingest_realtime(db: Session, data: RealTimeIn):
    train = crud.create_train_if_not_exists(db, data.train_number)
    station = None
    if data.station_code:
        station = crud.create_station_if_not_exists(db, data.station_code)
    rs = crud.add_realtime_status(db, train, station, data.timestamp, data.lat, data.lon, data.speed_kmph, data.note)
    return rs
