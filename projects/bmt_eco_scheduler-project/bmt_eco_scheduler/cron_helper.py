# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from croniter import croniter


def should_trigger_event(
    cron: str,
    now: datetime,
    delta: int,
):
    """
    Given a cron expression, a datetime object, and a delta in seconds, identify that
    the datetime object match the cron expression within the delta. The datetime
    has to later than the cron expression.

    :param cron: A cron expression in string.
    :param now: A datetime object in UTC.
    :param delta: A delta in seconds.
    """
    iter = croniter(cron, now)
    previous = iter.get_prev(datetime)
    return now - previous <= timedelta(seconds=delta)
