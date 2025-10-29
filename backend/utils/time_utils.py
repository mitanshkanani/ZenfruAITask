# backend/utils/time_utils.py
from datetime import datetime, timedelta

TIME_FORMAT = "%H:%M"


def str_to_time(time_str: str) -> datetime.time:
    """Converts 'HH:MM' string to datetime.time object"""
    return datetime.strptime(time_str, TIME_FORMAT).time()


def time_to_str(time_obj: datetime.time) -> str:
    """Converts datetime.time object to 'HH:MM' string"""
    return time_obj.strftime(TIME_FORMAT)


def is_overlap(start1: datetime, end1: datetime, start2: datetime, end2: datetime) -> bool:
    """
    Checks if two datetime ranges overlap
    """
    return max(start1, start2) < min(end1, end2)


def add_minutes(time_obj: datetime, minutes: int) -> datetime:
    """Add minutes to a datetime object"""
    return time_obj + timedelta(minutes=minutes)
