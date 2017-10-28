from datetime import datetime, timedelta
from operator import itemgetter
import time
import calendar
import laboris.settings as s
from enum import Enum
import pprint
from collections import OrderedDict

global args
global data


class Report(Enum):
    SUMMARY = 0
    TIMES = 1
    PROJECT = 2
    ACTIVE = 3
    DAY = 4
    WEEK = 5


def report(report, a, d):
    global args
    global data
    args = a
    data = d
    if "clear" in args:
        print("\033[2J", end='')
        print("\033[H", end='')
    if "monitor" in args or "live" in args:
        live(report)
    else:
        display(False, report)


def display(reset, report):
    if report is Report.ACTIVE:
        active(reset)
    elif report is Report.TIMES:
        times(reset)
    elif report is Report.DAY:
        pass
        #  day(reset)
    elif report is Report.SUMMARY:
        summary(reset)


def summary(reset):
    global args, data
    count = OrderedDict()
    count["No Project"] = [0, 0, 0, 0]
    for task in s._pending:
        if len(task.project) == 0:
            count["No Project"][0] += 1
            count["No Project"][1] += 1
            count["No Project"][3] += task.get_age()
        for proj in task.project:
            if proj in count.keys():
                count[proj][0] += 1
                count[proj][1] += 1
                count[proj][3] += task.get_age()
            else:
                count[proj] = [1, 1, 0, 0]
                count[proj][3] += task.get_age()
    for task in s._done:
        if len(task.project) == 0:
            count["No Project"][0] += 1
            count["No Project"][2] += 1
            count["No Project"][3] += task.get_age()
        for proj in task.project:
            if proj in count.keys():
                count[proj][0] += 1
                count[proj][2] += 1
                count[proj][3] += task.get_age()
            else:
                count[proj] = [1, 0, 1, 0]
                count[proj][3] += task.get_age()
    size = [7, 9, 7, 8, 30]
    for key in count.keys():
        size[0] = max(size[0], len(key))
    title = [
        "Project", "Remaining", "Avg Age", "Complete",
        "0%                        100%"
    ]
    for i, t in enumerate(title):
        print(
            "{}{:{}}{} ".format(
                s._theme.get_color("title"), t, size[i], s._theme.reset()),
            end='')
    print()
    index = 0
    for key, val in count.items():
        val[3] = int(val[3] / val[0])
        output = "{:{}} ".format(key, size[0])
        output += "{:{}} ".format(val[2], size[1])
        tmp = str()
        if val[3] < 60:
            tmp += val[3] + "s"
        elif val[3] < 3600:
            tmp += int(val[3] / 60) + "m"
        elif val[3] < 86400:
            tmp += "%i" % int(val[3] / 3600) + "h"
        elif val[3] < 604800:
            tmp += int(val[3] / 86400) + "d"
        elif val[3] < 2628000:
            tmp += int(val[3] / 604800) + "W"
        elif val[3] < 31540000:
            tmp += int(val[3] / 2628000) + "M"
        else:
            tmp += "%i" % int(val[3] / 31540000) + "Y"
        output += "{:>{}} ".format(tmp, size[2])
        output += "{:>{}.0%} ".format(val[2] / val[0], size[3])
        output += s._theme.get_color("report.summary.completed")
        for i in range(0, 30):
            if i <= int(30 * (val[2] / val[0])):
                output += "\u2588"
            else:
                output += " "
        output += s._theme.reset()
        if index % 2 == 0:
            print(output)
        else:
            print(s._theme.bg() + output + s._theme.reset())
        index += 1
    line_count = len(count)
    line_count += 1
    if reset is True:
        print("\033[{}F".format(line_count), end='')
    #  pprint.pprint(count)


def times(reset):
    global args, data
    start, end = get_range(args)
    count = 0
    print_data = OrderedDict()
    size = [0, 0, 0, 0]
    total = 0
    for task in s._pending:
        for t in task.times:
            if t.start > start and t.start < end:
                if t.start.date() not in print_data.keys():
                    print_data[t.start.date()] = [0]
                print_data[t.start.date()].append([
                    task.description,
                    t.print_start(True),
                    t.print_end(True),
                    t.print_duration(True)
                ])
                print_data[t.start.date()][0] += t.get_duration()
                total += t.get_duration()
    for task in s._done:
        for t in task.times:
            if t.start > start and t.start < end:
                if t.start.date() not in print_data.keys():
                    print_data[t.start.date()] = [0]
                print_data[t.start.date()].append([
                    task.description,
                    t.print_start(True),
                    t.print_end(True),
                    t.print_duration(True)
                ])
                print_data[t.start.date()][0] += t.get_duration()
                total += t.get_duration()
    for val in print_data.values():
        for entry in val[1:]:
            size[0] = max(size[0], len(entry[0]))
            size[1] = max(size[1], len(entry[1]))
            size[2] = max(size[2], len(entry[2]))
            size[3] = max(size[3], len(entry[3]))
    print_data = sorted(print_data.items())
    for key, val in print_data:
        print("{}{:{}}{}".format(
            s._theme.get_color("title"),
            key.strftime("%a %b %d, %Y"), sum(size) + 9, s._theme.reset()))
        for i, entry in enumerate(val[1:]):
            if i % 2 == 0:
                fmt = "{:{}} {:{}} {:{}} {:{}}"
            else:
                fmt = s._theme.bg(
                ) + "{:{}} {:{}} {:{}} {:{}}" + s._theme.reset()
            print(
                fmt.format(entry[0], size[0] + 2, entry[1], size[1] + 2, entry[
                    2], size[2] + 2, entry[3], size[3]))
            count += 1
        sub_m, sub_s = divmod(val[0], 60)
        sub_h, sub_m = divmod(sub_m, 60)
        print("{:{}}{}{:>{}}{}".format(
            str(),
            sum(size) + 9 - size[3],
            s._theme.get_color("title"), "{:02}:{:02}:{:02}".format(
                sub_h, sub_m, sub_s), size[3], s._theme.reset()))
        count += 2
    m, sec = divmod(total, 60)
    h, m = divmod(m, 60)
    print("\n{}{:<{}}{:>{}}{}".format(
        s._theme.get_color("title"), "Total:", size[0] + size[1] + size[2] + 9,
        "{:02}:{:02}:{:02}".format(h, m, sec), size[3], s._theme.reset()))
    count += 2
    if reset is True:
        print("\033[{}F".format(count), end='')


def active(reset):
    global args, data
    count = 0
    for task in s._pending:
        if task.active is True:
            count += 3
            print("{}Task {} \'{}\' [{}]{}".format(
                s._theme.get_color("start"), task.id, task.description,
                task.times[-1].print_duration(True), s._theme.reset()))
            print("{}Start:   {}{}".format(
                s._theme.get_color("start"), task.times[-1].print_start(
                    "%I:%M:%S %p"), s._theme.reset()))
            print("{}Current: {}{}".format(
                s._theme.get_color("start"),
                time.strftime("%I:%M:%S %p"), s._theme.reset()))
    if count == 0:
        count += 1
        print("{}No Active Tasks{}".format(
            s._theme.get_color("warn"), s._theme.reset()))
    if reset is True:
        print("\033[{}F".format(count), end='')


def get_range(args):
    start = datetime.now().replace(hour=0, minute=0, second=0)
    end = datetime.now().replace(hour=23, minute=59, second=59)
    if "yesterday" in args:
        start -= timedelta(days=1)
        end -= timedelta(days=1)
    elif "week" in args:
        start -= timedelta(days=start.weekday())
        end = start + timedelta(days=7)
    elif "lastweek" in args:
        start -= timedelta(days=start.weekday() - 7)
        end = start + timedelta(days=7)
    elif "all" in args:
        start = datetime(year=1, month=1, day=1)
    elif "month" in args:
        start -= timedelta(days=start.day - 1)
        end = start + timedelta(days=calendar.monthrange(
            start.year, start.month)[1])
    elif "lastmonth" in args:
        start = start.replace(day=1, month=start.month - 1)
        end = start + timedelta(days=calendar.monthrange(
            start.year, start.month)[1])
    elif "year" in args:
        start = start.replace(day=1, month=1)
        end = start + timedelta(days=365)
    return start, end


def live(report):
    try:
        while True:
            display(True, report)
            time.sleep(1)
    except KeyboardInterrupt:
        display(False, report)
        pass


def is_report(arg):
    reports = {
        "summary": Report.SUMMARY,
        "times": Report.TIMES,
        "project": Report.PROJECT,
        "active": Report.ACTIVE,
        "day": Report.DAY,
        "week": Report.WEEK
    }
    for a in arg:
        if a.lower() in reports.keys():
            arg.remove(a)
            return reports[a.lower()]
    return None
