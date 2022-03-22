import json
from datetime import datetime

def check_status(social_media_platform: str, status_type: str) -> bool:
    with open('/data/listeningsquad/daily_status.json') as f:
        jobj = json.load(f)

    latest_collection_date = jobj[social_media_platform][status_type]
    latest_collection_dt_obj = datetime.strptime(reddit_latest_collection_date, "%Y-%m-%d").date()

    if latest_collection_dt_obj == datetime.now().date():
        return True
    return False