from pydantic import BaseModel
from typing import Optional, List
import datetime

# stations & trains
class StationCreate(BaseModel):
    code: str
    name: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class StationOut(StationCreate):
    id: int
    class Config:
        orm_mode = True

class TrainCreate(BaseModel):
    train_number: str
    name: Optional[str] = None

class TrainOut(TrainCreate):
    id: int
    class Config:
        orm_mode = True

# schedule
class SchedulePointCreate(BaseModel):
    train_number: str
    station_code: str
    arrival_time: Optional[datetime.datetime] = None
    departure_time: Optional[datetime.datetime] = None
    sequence: int

class UploadScheduleResult(BaseModel):
    rows: int
    created_trains: int
    created_stations: int

# realtime
class RealTimeIn(BaseModel):
    train_number: str
    timestamp: datetime.datetime
    station_code: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    speed_kmph: Optional[float] = None
    note: Optional[str] = None

class PredictionOut(BaseModel):
    train_number: str
    station_code: Optional[str]
    predicted_delay_minutes: float
    generated_at: datetime.datetime

# priorities
class PriorityIn(BaseModel):
    train_number: str
    priority: int

# optimize request
class OptimizeRequest(BaseModel):
    current_time: Optional[datetime.datetime] = None

# recommendation
class Recommendation(BaseModel):
    train_number: str
    action: str
    details: dict
