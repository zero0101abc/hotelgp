from app.utils.auth import hash_password
from datetime import datetime

def generate_booking_id() -> str:
    import random
    return f"BK-{random.randint(1000, 9999)}"

def format_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")