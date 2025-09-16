from datetime import datetime
from typing import Optional
import dateutil.parser

def parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if ts is None:
        return None
    if isinstance(ts, datetime):
        return ts
    try:
        return dateutil.parser.isoparse(ts)
    except Exception:
        return None
