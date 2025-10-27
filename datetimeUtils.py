from datetime import datetime
from dateutil import parser


def is_in_date_time_format(string: str, format: str) -> bool:
    try:
        datetime.strptime(string, format)
        return True
    except Exception:
        return False


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """
    Function for parsing of date and time given in arbitrary format
    """
    try:
        return parser.parse(f"{date_str} {time_str}")
    except Exception as e:
        # print(f"Failed to parse: {date_str} {time_str} → {e}")
        # return None
        raise e
