"""
Real-time adaptation stitches the other AI modules:
- collects upcoming schedule points
- fetches latest real-time info
- computes predictions
- detects conflicts
- runs throughput optimization
- returns recommendations
"""
from datetime import datetime, timedelta
from typing import List, Dict
from ..crud import get_upcoming_schedule_points, get_latest_realtime_for_train, get_priority_for_train, store_prediction # type: ignore
from .delay_prediction import predict_delay_from_schedule_and_actual, predict_delay_with_features
from .conflict_detection import detect_conflicts
from .throughput_optimization import optimize_throughput

def run_adaptation(db, current_time: datetime):
    # 1. get upcoming schedule points (next N)
    upcoming_sp = get_upcoming_schedule_points(db, after_time=current_time)
    # transform to simple dict list
    upcoming = []
    for sp in upcoming_sp:
        train = sp.train
        station = sp.station
        scheduled = sp.arrival_time or sp.departure_time
        # latest realtime
        rt = get_latest_realtime_for_train(db, train.id)
        predicted_delay = 0.0
        # If latest realtime and it's close to scheduled station, compute observed delay
        if rt and scheduled:
            # if reported_time after scheduled - observed delay
            predicted_delay = predict_delay_from_schedule_and_actual(scheduled, rt.reported_time)
            # store prediction (persist)
            store_prediction(db, train, station, predicted_delay)
        # fallback: features-based prediction if no realtime
        else:
            features = {'base_delay': 0.0}
            if rt and rt.speed_kmph:
                features['speed_kmph'] = rt.speed_kmph
            predicted_delay = predict_delay_with_features(features)
            store_prediction(db, train, station, predicted_delay)
        priority = get_priority_for_train(db, train.id)
        upcoming.append({
            "train_number": train.train_number,
            "train_id": train.id,
            "station_code": station.code if station else "UNKNOWN",
            "scheduled": scheduled,
            "predicted_delay_minutes": predicted_delay,
            "priority": priority
        })
    # 2. detect conflicts
    conflicts = detect_conflicts(upcoming)
    # 3. throughput optimization recommendations
    throughput_recs = optimize_throughput(upcoming)
    # 4. collate recommendations (convert to unified format)
    recs = []
    # conflicts -> create hold recommendations if recommended_to_hold present
    for c in conflicts:
        recs.append({
            "train_number": c.get("recommended_to_hold"),
            "action": "hold_due_to_conflict",
            "details": {k: v for k, v in c.items() if k not in ("recommended_to_hold",)}
        })
    # add throughput recs
    recs.extend(throughput_recs)
    # remove None train entries & deduplicate preserving order
    seen = set()
    final = []
    for r in recs:
        tn = r.get("train_number")
        if not tn or tn in seen:
            continue
        seen.add(tn)
        final.append(r)
    return {
        "generated_at": datetime.utcnow(),
        "recommendations": final,
        "conflicts_count": len(conflicts),
        "throughput_recs_count": len(throughput_recs)
    }
