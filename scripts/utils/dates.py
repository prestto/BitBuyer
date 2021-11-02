"""
Date functions needed when interacting with apis
"""
from datetime import datetime


def round_hour(dt: datetime) -> datetime:
    """round down the hour"""
    return dt.replace(minute=0, second=0, microsecond=0)


def strf_twitter(dt: datetime) -> str:
    """convert datetime to string compatible with twitter api"""
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
