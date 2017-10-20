from datetime import datetime
import time
import settings as s
from enum import Enum

global args
global data
global pdata


class Report(Enum):
    SUMMARY = 0
    TIMES = 1
    PROJECT = 2
    ACTIVE = 3


def report(report, a, d):
    global args
    global data
    global pdata
    args = a
    data = d
    pdata = list()
    if report is Report.ACTIVE:
        active()
    elif report is Report.TIMES:
        times()
    if "clear" in args:
        print("\033[2J", end='')
        print("\033[H", end='')
    if "monitor" in args or "live" in args:
        live()
    else:
        display()


def times():
    global args, data, pdata
    for task in s._pending:
        for t in task.times:
            if t.is_done() is True:
                pdata.append([
                    "{} {} {} {}", task.description,
                    t.print_start(True),
                    t.print_end(True),
                    t.print_duration(True)
                ])
            else:
                pdata.append([
                    "{} {} {} {}", task.description,
                    t.print_start(True), (t.print_end, True), (t.print_duration,
                                                               True)
                ])


def active():
    global args, data, pdata
    has_task = False
    for task in s._pending:
        if task.active is True:
            has_task = True
            pdata.append([
                "{}Task {} \'{}\' [{}]{}",
                s._theme.get_color("start"), task.id, task.description,
                (task.times[-1].print_duration, True),
                s._theme.reset()
            ])
            pdata.append([
                "    {}Start:   {}{}",
                s._theme.get_color("start"), (task.times[-1].print_start,
                                              "%I:%M:%S %p"),
                s._theme.reset()
            ])
            pdata.append([
                "    {}Current: {}{}",
                s._theme.get_color("start"), (time.strftime, "%I:%M:%S %p"),
                s._theme.reset()
            ])
            if has_task is False:
                pdata.append([
                    "{}No Active Tasks{}",
                    s._theme.get_color("warn"),
                    s._theme.reset()
                ])


def live():
    try:
        while True:
            display(True)
            time.sleep(1)
    except KeyboardInterrupt:
        display()
        pass


def display(reset=False):
    global pdata
    for cmd in pdata:
        data = list()
        for entry in cmd:
            if type(entry) is tuple:
                data.append(entry[0](*entry[1:]))
            else:
                data.append(entry)
        print(data[0].format(*data[1:]))
    if reset is True:
        print("\033[{}F".format(len(pdata)), end='')


def is_report(arg):
    reports = {
        "summary": Report.SUMMARY,
        "times": Report.TIMES,
        "project": Report.PROJECT,
        "active": Report.ACTIVE
    }
    for a in arg:
        if a.lower() in reports.keys():
            arg.remove(a)
            return reports[a.lower()]
    return None
