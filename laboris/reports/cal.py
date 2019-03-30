import datetime
import calendar
import laboris.task as ltask
from laboris.color import Attr
from laboris.config import CONFIG

from pprint import pprint

MONTHS = [('january', 'jan'), ('feburary', 'feb'), ('march', 'mar'), ('april',
                                                                      'apr'),
          ('may', 'may'), ('june', 'jun'), ('july', 'jul'), ('august', 'aug'),
          ('september',
           'sep'), ('october', 'oct'), ('november', 'nov'), ('december', 'dec')]


def cal_report(args):
    start = None
    end = None
    count = None
    for arg in args:
        for i, mon in enumerate(MONTHS):
            if arg in mon:
                if start is None:
                    start = i + 1
                else:
                    end = i + 1
        if arg in "0123456789":
            count = int(arg)
    if start is None:
        start = datetime.date.today().month
    elif end is None:
        end = start
    if count is not None:
        end = start + count - 1
    if end is None:
        end = datetime.date.today().month
    if end < start:
        end += 12
    months = []
    year = 2019
    dues = {}
    for uuid, task in ltask.PENDING.items():
        if task['dueDate'] is not None:
            date = datetime.datetime.fromtimestamp(task['dueDate']).date()
            if date.isoformat() not in dues:
                dues[date.isoformat()] = task['urg']
            elif dues[date.isoformat()] < task['urg']:
                dues[date.isoformat()] = task['urg']
    for month in range(start, end + 1):
        if month >= 13:
            year = 2019
            month -= 12
        mon = [
            "{:^20}".format(MONTHS[month - 1][0].title()),
            "Su Mo Tu We Th Fr Sa"
        ]
        for day in range(
                calendar.monthrange(datetime.date.today().year, month)[1]):
            day = datetime.date(year=year, month=month, day=day + 1)
            wday = (day.weekday() + 1) % 7
            if wday == 0 or len(mon) == 2:
                if len(mon) > 2:
                    mon[-1] = ' '.join(mon[-1])
                mon.append(['  '] * 7)

            if day.isoformat() in dues:
                mon[-1][wday] = Attr('{:2}'.format(day.day),
                                     CONFIG.get_color('urgency',
                                                      dues[day.isoformat()]))
            elif datetime.date.today() == day:
                mon[-1][wday] = Attr('{:2}'.format(day.day),
                                     CONFIG.get_color('status.active'))
            else:
                mon[-1][wday] = '{:2}'.format(day.day)

        mon[-1] = ' '.join(mon[-1])
        months.append(mon)
        for lin in mon:
            print(lin)
