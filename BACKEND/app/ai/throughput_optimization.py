"""
Very small prototype of throughput optimization:
Given a set of upcoming arrivals for station sections, try to minimize makespan by recommending
small holds/advances based on priority. This is greedy and meant for hackathon demo.
"""
from datetime import timedelta

def optimize_throughput(upcoming):
    """
    upcoming: list of dicts:
      - train_number
      - station_code
      - scheduled (datetime)
      - priority (int)
      - predicted_delay_minutes (optional)
    Returns recommendations: list of dict {train_number, action, details}
    """
    recs = []
    # For each station, ensure spacing between arrivals >= MIN_GAP
    MIN_GAP_MINUTES = 3
    from collections import defaultdict
    by_station = defaultdict(list)
    for item in upcoming:
        by_station[item['station_code']].append(item)
    for station, items in by_station.items():
        # sort by scheduled + predicted delay
        def eff_time(it):
            t = it['scheduled']
            if 'predicted_delay_minutes' in it and it['predicted_delay_minutes'] is not None:
                t = t + timedelta(minutes=float(it['predicted_delay_minutes']))
            return t
        items.sort(key=eff_time)
        for i in range(1, len(items)):
            prev = items[i-1]
            cur = items[i]
            gap = (eff_time(cur) - eff_time(prev)).total_seconds() / 60.0
            if gap < MIN_GAP_MINUTES:
                # propose hold for lower-priority train (usually cur)
                if cur.get('priority',1) <= prev.get('priority',1):
                    hold = MIN_GAP_MINUTES - gap + 1  # add small buffer
                    recs.append({
                        "train_number": cur['train_number'],
                        "action": "hold_at_station",
                        "details": {
                            "station_code": station,
                            "hold_seconds": int(hold * 60),
                            "reason": f"maintain {MIN_GAP_MINUTES} min gap behind {prev['train_number']}"
                        }
                    })
                else:
                    # try to suggest speed up prev if possible (mock)
                    recs.append({
                        "train_number": prev['train_number'],
                        "action": "increase_speed",
                        "details": {
                            "target_speed_kmph_increase": 5,
                            "reason": f"higher priority than {cur['train_number']}"
                        }
                    })
    # deduplicate by train_number keeping first
    seen = set()
    final = []
    for r in recs:
        if r['train_number'] not in seen:
            seen.add(r['train_number'])
            final.append(r)
    return final
