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

    def get_filename_suffix(self, period: str) -> str:
        try:
            from_date, to_date = self.get_daterange(period)
            interval = to_date - from_date
            suffix = ""
            suffix += from_date.strftime("%y%m%d")
            if interval != datetime.timedelta(0, 86399, 999999):  # > 1 day
                suffix += to_date.strftime("_%y%m%d")
            return suffix
        except Exception as e:
            raise e

    def get_report_title(self, period, reportType="Report") -> str:
        try:
            start, end = self.get_daterange(period)
            interval = end - start
            if interval == datetime.timedelta(0, 86399, 999999):
                title = "Daily " + reportType + " - " + end.strftime("%d-%b-%y")
            elif interval == datetime.timedelta(6, 86399, 999999):
                title = "Weekly " + reportType + " - " + end.strftime("%d-%b-%y")
            elif (start.day == 1) and (end.day == calendar.monthrange(end.year, end.month)[1]) and (start.month == end.month):
                title = "Monthly " + reportType + " - " + end.strftime("%B %y")
            elif (start.day == 1) and (end.day == 15) and (start.month == end.month):
                title = "Fortnightly " + reportType + " - " + end.strftime("%B %y/1")
            elif (start.day == 16) and (end.day == calendar.monthrange(end.year, end.month)[1]) and (start.month == end.month):
                title = "Fortnightly " + reportType + " - " + end.strftime("%B %y/2")
            elif (start.strftime("%d%m") == "0101") and (end.strftime("%d%m") == "3112") and (start.strftime("%y") == end.strftime("%y")):
                title = "Yearly " + reportType + " - " + end.strftime("%Y")
            else:
                title = reportType + " - " + end.strftime("%d-%b-%y")
            return title
        except Exception:
            raise

    def get_truncated_daterange(self, period, includeToday=False) -> str:
        try:
            from_date, to_date = self.get_daterange(period)
            if from_date.date() == to_date.date():
                pass
            elif to_date > self._tz.localize(datetime.datetime.now()):
                if includeToday:
                    to_date, to_date = self.get_daterange("today")
                else:
                    to_date, to_date = self.get_daterange("yesterday")
            revised_period = from_date.strftime("%y%m%d-") + to_date.strftime("%y%m%d")
            return revised_period
        except Exception as e:
            raise e

    def get_dates_in_period(self, period: str):
        try:
            start_date, end_date = self.get_daterange(period)
            for n in range(int((end_date - start_date).days) + 1):
                yield start_date + datetime.timedelta(n)
        except Exception as e:
            raise e
