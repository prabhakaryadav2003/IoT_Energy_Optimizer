import time
import datetime


def now():
    return time.time()


def seconds_since(ts):
    return time.time() - ts


def minutes_since(ts):
    return (time.time() - ts) / 60.0


def current_hour():
    return datetime.datetime.now().hour


def current_slot(slot_minutes=15):
    now_dt = datetime.datetime.now()
    return now_dt.hour * (60 // slot_minutes) + now_dt.minute // slot_minutes


def current_time():
    return datetime.datetime.now()