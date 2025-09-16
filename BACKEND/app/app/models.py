from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Train(Base):
    __tablename__ = "trains"
    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)

    schedule_points = relationship("SchedulePoint", back_populates="train", cascade="all, delete-orphan")
    realtime_points = relationship("RealTimeStatus", back_populates="train", cascade="all, delete-orphan")
    priorities = relationship("TrainPriority", back_populates="train", uselist=False)

class Station(Base):
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    schedule_points = relationship("SchedulePoint", back_populates="station")

class SchedulePoint(Base):
    __tablename__ = "schedule_points"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), index=True)
    arrival_time = Column(DateTime, nullable=True, index=True)
    departure_time = Column(DateTime, nullable=True, index=True)
    sequence = Column(Integer, index=True)

    train = relationship("Train", back_populates="schedule_points")
    station = relationship("Station", back_populates="schedule_points")

class RealTimeStatus(Base):
    __tablename__ = "realtime_status"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), index=True, nullable=True)
    reported_time = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    speed_kmph = Column(Float, nullable=True)
    note = Column(String, nullable=True)

    train = relationship("Train", back_populates="realtime_points")
    station = relationship("Station")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), index=True, nullable=True)
    predicted_delay_minutes = Column(Float, nullable=True)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

class TrainPriority(Base):
    __tablename__ = "train_priorities"
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), unique=True)
    priority = Column(Integer, default=1)  # higher = more priority

    train = relationship("Train", back_populates="priorities")
