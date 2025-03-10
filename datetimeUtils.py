from datetime import datetime


def is_in_date_time_format(string: str, format: str) -> bool:
    try:
        datetime.strptime(string, format)
        return True
    except Exception:
        return False
