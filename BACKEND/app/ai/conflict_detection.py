"""
Conflict detection:
Given upcoming schedule points, detect collisions on the same 'station' (proxy for track section)
within a time window.
"""
from datetime import timedelta
from typing import List, Dict

CONFLICT_WINDOW_MINUTES = 5  # adjustable

def detect_conflicts(upcoming: List[Dict]) -> List[Dict]:
    """
    upcoming: list of dicts with keys:
      - train_number
      - station_code
      - scheduled (datetime)
      - predicted_delay_minutes (optional)
      - priority (int optional)
    Returns list of conflict dicts explaining conflicts.
    """
    conflicts = []
    n = len(upcoming)
    window = timedelta(minutes=CONFLICT_WINDOW_MINUTES)
    # group by station
    from collections import defaultdict
    by_station = defaultdict(list)
    for item in upcoming:
        by_station[item['station_code']].append(item)
    for station, items in by_station.items():
        items.sort(key=lambda x: x['scheduled'])
        for i in range(len(items)):
            a = items[i]
            for j in range(i+1, len(items)):
                b = items[j]
                # compute effective scheduled times considering predicted delay
                a_time = a['scheduled']
                b_time = b['scheduled']
                if 'predicted_delay_minutes' in a:
                    a_time = a_time + timedelta(minutes=float(a['predicted_delay_minutes']))
                if 'predicted_delay_minutes' in b:
                    b_time = b_time + timedelta(minutes=float(b['predicted_delay_minutes']))
                if abs((b_time - a_time).total_seconds()) <= window.total_seconds():
                    # conflict: choose lower priority train to be adjusted (default lower priority = later)
                    a_pr = a.get('priority', 1)
                    b_pr = b.get('priority', 1)
                    # choose to delay lower priority
                    if b_pr <= a_pr:
                        choice = b
                        other = a
                    else:
                        choice = a
                        other = b
                    conflicts.append({
                        "station_code": station,
                        "train_1": a['train_number'],
                        "train_2": b['train_number'],
                        "recommended_to_hold": choice['train_number'],
                        "reason": f"arrival within {CONFLICT_WINDOW_MINUTES} minutes; priority({a_pr} vs {b_pr})"
                    })
    return conflicts
