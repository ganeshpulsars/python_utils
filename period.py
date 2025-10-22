import datetime
import pytz
import calendar
import re

# from utils import safe_int


def month_list():
    mList = [
        ("jan", "January"),
        ("feb", "February"),
        ("mar", "March"),
        ("apr", "April"),
        ("may", "May"),
        ("jun", "June"),
        ("jul", "July"),
        ("aug", "August"),
        ("sep", "September"),
        ("oct", "October"),
        ("nov", "November"),
        ("dec", "December"),
    ]
    return mList


class Period:
    def __init__(self, tz=None):
        self._tz = pytz.timezone("UTC") if tz is None else tz

    def get_daterange(self, period: str):
        today = datetime.date.today()
        period = period.casefold()
        one_day = re.match(r"^([0-9]{6})$", period)
        one_month = re.match(r"^([0-9]{4}$)", period)
        one_year = re.match(r"^([0-9]{2})$", period)
        lastxdays = re.match(r"^lastxdays_([0-9]*)$", period)
        date_range = re.match(r"^([0-9]{6})-([0-9]{6})$", period)

        try:
            if period == "today":
                FirstDay = today
                LastDay = FirstDay
            elif period == "yesterday":
                FirstDay = today - datetime.timedelta(days=1)
                LastDay = FirstDay
            elif period == "thisweek":
                FirstDay = today - datetime.timedelta(days=today.weekday())  # Monday
                LastDay = FirstDay + datetime.timedelta(days=6)
            elif period == "lastweek":
                FirstDay = today - datetime.timedelta(days=(today.weekday() + 7))
                # Monday
                LastDay = FirstDay + datetime.timedelta(days=6)
            elif period == "thismonth":
                FirstDay = today.replace(day=1)
                LastDay = today.replace(day=calendar.monthrange(today.year, today.month)[1])
            elif period == "lastmonth":
                LastDay = today.replace(day=1) - datetime.timedelta(days=1)
                FirstDay = LastDay.replace(day=1)
            elif period == "thisfortnight":
                if today.day <= 15:
                    FirstDay = today.replace(day=1)
                    LastDay = today.replace(day=15)
                else:
                    FirstDay = today.replace(day=16)
                    LastDay = today.replace(day=calendar.monthrange(today.year, today.month)[1])
            elif period == "lastfortnight":
                if today.day <= 15:
                    LastDay = today.replace(day=1) - datetime.timedelta(days=1)
                    FirstDay = LastDay.replace(day=16)
                else:
                    FirstDay = today.replace(day=1)
                    LastDay = today.replace(day=15)
            elif lastxdays:
                # noof_days = safe_int(lastxdays.group(1), 1)
                noof_days = int(lastxdays.group(1))
                LastDay = today
                FirstDay = today - datetime.timedelta(days=noof_days)
            elif period == "eternity":  # dirty way to bypass filtering
                FirstDay = datetime.datetime(2000, 1, 1, 0, 0, 0)
                LastDay = datetime.datetime(2050, 12, 31, 23, 59, 59)
            elif one_day:
                f = one_day.group(1)
                FirstDay = datetime.datetime(int(f[0:2]) + 2000, int(f[2:4]), int(f[4:6]))
                LastDay = FirstDay
            elif one_month:
                f = one_month.group(1)
                FirstDay = datetime.datetime(int(f[0:2]) + 2000, int(f[2:4]), 1)
                LastDay = FirstDay.replace(day=calendar.monthrange(FirstDay.year, FirstDay.month)[1])
            elif one_year:
                f = one_year.group(1)
                FirstDay = datetime.datetime(int(f[0:2]) + 2000, 1, 1)
                LastDay = datetime.datetime(int(f[0:2]) + 2000, 12, 31)
            elif date_range:
                f = date_range.group(1)
                t = date_range.group(2)
                FirstDay = datetime.datetime(int(f[0:2]) + 2000, int(f[2:4]), int(f[4:6]))
                LastDay = datetime.datetime(int(t[0:2]) + 2000, int(t[2:4]), int(t[4:6]))
                if FirstDay > LastDay:
                    FirstDay, LastDay = LastDay, FirstDay
            else:
                raise ValueError(f"Invalid period: {period}")
        except Exception as e:
            raise e

        from_datetime = self._tz.localize(datetime.datetime.combine(FirstDay, datetime.time.min))
        to_datetime = self._tz.localize(datetime.datetime.combine(LastDay, datetime.time.max))

        return from_datetime, to_datetime
