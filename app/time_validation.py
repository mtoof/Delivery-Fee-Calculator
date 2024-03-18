from fastapi import HTTPException
from datetime import datetime,timezone
from dateutil.parser import isoparse
from . import consts

def invalid_date_time(value):
    if value.tzinfo is None:
        raise HTTPException(status_code = 400, detail="item 'time' is invalid, time zone is missing")
    elif value.utcoffset() != timezone.utc.utcoffset(value):
        raise HTTPException(status_code = 400, detail="Datetime is not in UTC.")
    
    if value.year < consts.MIN_YEAR:
        raise HTTPException(status_code=400, detail=f"Item 'time' is invalid, Year can't be less than {consts.MIN_YEAR}", 
                            headers={"Content-Type": "application/json"})