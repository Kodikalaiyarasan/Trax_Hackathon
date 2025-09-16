from sqlalchemy.orm import Session
from . import models
import datetime

# trains & stations
def get_train_by_number(db: Session, train_number: str):
    return db.query(models.Train).filter(models.Train.train_number == train_number).first()

def create_train_if_not_exists(db: Session, train_number: str, name: str = None):
    t = get_train_by_number(db, train_number)
    if t:
        return t
    t = models.Train(train_number=train_number, name=name)
    db.add(t); db.commit(); db.refresh(t)
    return t

def get_station_by_code(db: Session, code: str):
    return db.query(models.Station).filter(models.Station.code == code).first()

def create_station_if_not_exists(db: Session, code: str, name: str = None, lat=None, lon=None):
    s = get_station_by_code(db, code)
    if s:
        return s
    s = models.Station(code=code, name=name, lat=lat, lon=lon)
    db.add(s); db.commit(); db.refresh(s)
    return s

# schedule
def add_schedule_point(db: Session, train, station, arrival_time, departure_time, sequence):
    sp = models.SchedulePoint(train_id=train.id, station_id=station.id, arrival_time=arrival_time,
                              departure_time=departure_time, sequence=sequence)
    db.add(sp); db.commit(); db.refresh(sp)
    return sp

def get_upcoming_schedule_points(db: Session, after_time, limit=500):
    return db.query(models.SchedulePoint).filter(
        (models.SchedulePoint.arrival_time != None) | (models.SchedulePoint.departure_time != None)
    ).filter(
        (models.SchedulePoint.arrival_time >= after_time) | (models.SchedulePoint.departure_time >= after_time)
    ).order_by(models.SchedulePoint.arrival_time).limit(limit).all()

# realtime
def add_realtime_status(db: Session, train, station, timestamp, lat, lon, speed_kmph, note):
    rs = models.RealTimeStatus(train_id=train.id, station_id=(station.id if station else None),
                               reported_time=timestamp, lat=lat, lon=lon, speed_kmph=speed_kmph, note=note)
    db.add(rs); db.commit(); db.refresh(rs)
    return rs

def get_latest_realtime_for_train(db: Session, train_id: int):
    return db.query(models.RealTimeStatus).filter(models.RealTimeStatus.train_id == train_id)\
        .order_by(models.RealTimeStatus.reported_time.desc()).first()

# prediction storage
def store_prediction(db: Session, train, station, predicted_delay_minutes):
    pred = models.Prediction(train_id=train.id, station_id=(station.id if station else None),
                             predicted_delay_minutes=predicted_delay_minutes,
                             generated_at=datetime.datetime.utcnow())
    db.add(pred); db.commit(); db.refresh(pred)
    return pred

# priority
def upsert_priority(db: Session, train, priority: int):
    p = db.query(models.TrainPriority).filter(models.TrainPriority.train_id == train.id).first()
    if p:
        p.priority = priority
        db.add(p); db.commit(); db.refresh(p)
        return p
    p = models.TrainPriority(train_id=train.id, priority=priority)
    db.add(p); db.commit(); db.refresh(p)
    return p

def get_priority_for_train(db: Session, train_id: int):
    p = db.query(models.TrainPriority).filter(models.TrainPriority.train_id == train_id).first()
    return p.priority if p else 1
