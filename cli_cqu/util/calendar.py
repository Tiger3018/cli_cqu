"""制作日历日程"""
import re
import uuid

from copy import deepcopy
from datetime import datetime
from datetime import date
from typing import *

from icalendar import Calendar
from icalendar import Event

from ..data.schedule import Schedule
from ..model import Course, ExperimentCourse
from ..util.datetime import materialize_calendar, VTIMEZONE

__all__ = ("make_ical", )


def make_ical(courses: List[Union[Course, ExperimentCourse]], start: date,
              schedule: Schedule) -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//Zombie110year//CLI CQU//")
    cal.add("version", "2.0")
    cal.add_component(VTIMEZONE)
    for course in courses:
        for ev in build_event(course, start, schedule):
            cal.add_component(ev)
    return cal


def build_event(course: Union[Course, ExperimentCourse], start: date,
                schedule: Schedule) -> List[Event]:
    proto = Event()
    proto.add("summary", course.identifier)
    proto.add("location", course.location)
    if isinstance(course, Course):
        proto.add("description", f"教师：{course.teacher}")
    elif isinstance(course, ExperimentCourse):
        proto.add(
            "description",
            f"教师：{course.teacher}；值班教师：{course.hosting_teacher}；\n项目：{course.project_name}"
        )
    else:
        raise TypeError(
            f"{course} 需要是 Course 或 ExperimentCourse，但却是 {type(course)}")

    results = []
    weeks = course.week_schedule.split(
        ",") if "," in course.week_schedule else [course.week_schedule]
    for week in weeks:
        ev: Event = deepcopy(proto)
        t_week = re.match(r"^(\d+)", week)[1]
        t_lesson = course.day_schedule
        first_lesson = materialize_calendar(t_week, t_lesson, start, schedule)
        dt_start, dt_end = first_lesson

        ev.add("dtstart", dt_start)
        ev.add("dtend", dt_end)

        # 解析周规则
        if "-" in week:
            a, b = week.split("-")
            count = int(b) - int(a) + 1
        else:
            count = 1
        ev.add("rrule", {"freq": "weekly", "count": count})
        results.append(ev)

        # RFC 5545 要求 VEVENT 必须存在 dtstamp 与 uid 属性
        ev.add('dtstamp', datetime.utcnow())
        namespace = uuid.UUID(
            bytes=int(dt_start.timestamp()).to_bytes(length=8, byteorder='big')
            + int(dt_end.timestamp()).to_bytes(length=8, byteorder='big'))
        ev.add('uid',
               uuid.uuid3(namespace, f"{course.identifier}-{course.teacher}"))
    return results


# depracated
def make_range(string: str) -> List[Tuple[str]]:
    """将 ``1-9``, ``1-4,6-9`` 这样的字符串解析为最小单位（a-b 或 n）序列。
    源字符串中 ``s-e`` 表示一个闭区间

    >>> make_range("1")
    [1]
    >>> make_range("1-9")
    [(1, 9)]
    >>> make_range("1,3-9")
    [1, (3, 9)]
    """
    ans = list()
    for component in string.split(","):
        if re.fullmatch(r"\d+", component):
            ans.append(int(component))
        elif re.fullmatch(r"\d+-\d+", component):
            r = tuple([int(x) for x in component.split("-")])
            ans.append(r)
        else:
            raise ValueError(f"字符串 {string} 格式有问题，{component} 无法解析")
    return ans
