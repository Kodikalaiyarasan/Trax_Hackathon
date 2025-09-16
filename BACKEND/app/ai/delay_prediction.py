"""
Delay prediction module.

For hackathon prototype this provides:
 - simple deterministic baseline: predicted_delay = observed_delay (if actual known)
 - if only recent location & schedule exists, compute ETA vs schedule to estimate delay
 - placeholder for plugging in ML model later (sklearn, xgboost, etc.)
"""
from datetime import datetime
from typing import Optional
import math

def predict_delay_from_schedule_and_actual(scheduled_time: datetime, actual_time: datetime) -> float:
    """
    Return predicted delay in minutes (float). Non-negative.
    """
    delay_min = (actual_time - scheduled_time).total_seconds() / 60.0
    return max(delay_min, 0.0)

def predict_delay_with_features(features: dict) -> float:
    """
    Placeholder for ML model. features can contain hour, weekday, historical_avg, speed, distance_to_station etc.
    We'll implement a simple heuristic: base + speed_factor.
    """
    base = float(features.get('base_delay', 0.0))
    speed = features.get('speed_kmph', None)
    if speed is None:
        return base
    # If speed low -> increase delay; if high -> reduce
    if speed < 30:
        factor = 1.5
    elif speed < 50:
        factor = 1.2
    else:
        factor = 0.9
    return max(0.0, base * factor)
