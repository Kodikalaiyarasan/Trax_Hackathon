from sqlalchemy.orm import Session
from .. import crud
import pandas as pd
import io
from typing import Tuple

def import_schedule_csv(db: Session, file_bytes: bytes) -> Tuple[int, int, int]:
    """
    CSV expected columns:
      train_number, train_name (opt), station_code, station_name (opt),
      arrival_time (ISO optional), departure_time (ISO optional), sequence, lat (opt), lon (opt)
    Returns: rows, created_trains, created_stations
    """
    df = pd.read_csv(io.BytesIO(file_bytes))
    rows = 0
    created_trains = set()
    created_stations = set()
    for _, row in df.iterrows():
        rows += 1
        train_number = str(row['train_number'])
        train_name = row.get('train_name', None)
        station_code = str(row['station_code'])
        station_name = row.get('station_name', station_code)
        lat = row.get('lat', None) if 'lat' in row else None
        lon = row.get('lon', None) if 'lon' in row else None
        arrival_time = None
        departure_time = None
        if 'arrival_time' in row and pd.notna(row['arrival_time']):
            arrival_time = pd.to_datetime(row['arrival_time']).to_pydatetime()
        if 'departure_time' in row and pd.notna(row['departure_time']):
            departure_time = pd.to_datetime(row['departure_time']).to_pydatetime()
        sequence = int(row['sequence']) if 'sequence' in row and not pd.isna(row['sequence']) else 0

        train = crud.create_train_if_not_exists(db, train_number, name=train_name)
        station = crud.create_station_if_not_exists(db, station_code, name=station_name, lat=lat, lon=lon)
        crud.add_schedule_point(db, train, station, arrival_time, departure_time, sequence)
        created_trains.add(train.id)
        created_stations.add(station.id)
    return rows, len(created_trains), len(created_stations)
