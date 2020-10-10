import pytest
from datetime import datetime
from datetime import date
from datetime import timezone, timedelta
from cli_cqu.util.datetime import materialize_calendar
from cli_cqu.data.schedule import ShaPingBaSchedule, New2020Schedule
from typing import Tuple
START = "2020-02-17"

def dt(*args):
    return datetime(*args, tzinfo=timezone(timedelta(hours=8), "Asia/Shanghai"))

@pytest.mark.parametrize("tw, tl, ex", [
    ("1", "一[1-2节]", (dt(2020, 2, 17, 8), dt(2020, 2, 17, 9, 40))),
    ("1", "一[3-4节]", (dt(2020, 2, 17, 10, 10), dt(2020, 2, 17, 11, 50))),
    ("1", "一[5-6节]", (dt(2020, 2, 17, 14, 30), dt(2020, 2, 17, 16, 10))),
    ("1", "一[7-8节]", (dt(2020, 2, 17, 16, 40), dt(2020, 2, 17, 18, 20))),
    ("1", "一[9-11节]", (dt(2020, 2, 17, 19, 30), dt(2020, 2, 17, 22, 5))),
    ("1", "一[9-12节]", (dt(2020, 2, 17, 19, 30), dt(2020, 2, 17, 23, 59))),
    ("1", "一[14节]", (dt(2020, 2, 17, 8), dt(2020, 2, 17, 23, 59))),
    ("1", "二[1-2节]", (dt(2020, 2, 18, 8), dt(2020, 2, 18, 9, 40))),
    ("1", "二[3-4节]", (dt(2020, 2, 18, 10, 10), dt(2020, 2, 18, 11, 50))),
    ("1", "二[5-6节]", (dt(2020, 2, 18, 14, 30), dt(2020, 2, 18, 16, 10))),
    ("1", "二[7-8节]", (dt(2020, 2, 18, 16, 40), dt(2020, 2, 18, 18, 20))),
    ("1", "二[9-11节]", (dt(2020, 2, 18, 19, 30), dt(2020, 2, 18, 22, 5))),
    ("1", "二[9-12节]", (dt(2020, 2, 18, 19, 30), dt(2020, 2, 18, 23, 59))),
    ("1", "二[14节]", (dt(2020, 2, 18, 8), dt(2020, 2, 18, 23, 59))),
    ("2", "二[1-2节]", (dt(2020, 2, 25, 8), dt(2020, 2, 25, 9, 40))),
    ("2", "二[3-4节]", (dt(2020, 2, 25, 10, 10), dt(2020, 2, 25, 11, 50))),
    ("2", "二[5-6节]", (dt(2020, 2, 25, 14, 30), dt(2020, 2, 25, 16, 10))),
    ("2", "二[7-8节]", (dt(2020, 2, 25, 16, 40), dt(2020, 2, 25, 18, 20))),
    ("2", "二[9-11节]", (dt(2020, 2, 25, 19, 30), dt(2020, 2, 25, 22, 5))),
    ("2", "二[9-12节]", (dt(2020, 2, 25, 19, 30), dt(2020, 2, 25, 23, 59))),
    ("2", "二[14节]", (dt(2020, 2, 25, 8), dt(2020, 2, 25, 23, 59))),
])

@pytest.mark.parametrize("newSchWee, newSchLec, newSchDur", [
    ("7", "二[3-4节]", (dt(2020, 10, 13, 10, 30), dt(2020, 10, 13, 12, 10))),
    ("7", "三[10-13节]", (dt(2020, 10, 14, 19, 00), dt(2020, 10, 14, 23, 59))),
])

def test_materialize_calendar(tw: str, tl: str, ex: Tuple[dt, dt], newSchWee: str, newSchLec: str, newSchDur: Tuple[dt, dt]):
    assert ex == materialize_calendar(tw, tl, start=date(2020, 2, 17), schedule=ShaPingBaSchedule())
    assert newSchDur == materialize_calendar(newSchWee, newSchLec, start = date(2020, 8, 31), schedule = New2020Schedule())
