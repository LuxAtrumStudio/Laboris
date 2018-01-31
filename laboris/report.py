import time
import calendar
import os
import random
import math
import laboris.settings as sett
import laboris.printer as printer

from laboris.table import Table
import laboris.display as display
from datetime import datetime, timedelta


def monitor(args):
    args.monitor = False
    try:
        while True:
            report(args, True)
            time.sleep(1)
    except KeyboardInterrupt:
        report(args, False)


def report(args, reset=False):
    if args.report is None:
        printer.print_error('report', "Must specify a report type.")
        return
    if args.monitor is True:
        monitor(args)
        return
    if args.clear is True:
        print('\033[2J\033[H', end='')
    if args.report == 'summary':
        summary(args, reset)
    elif args.report == 'active':
        active(args, reset)
    elif args.report == 'times':
        times(args, reset)
    elif args.report == 'burndown':
        burndown(args, reset)
    elif args.report == 'graph':
        graph(args, reset)
    elif args.report == 'calendar':
        cal(args, reset)


def summary(args, reset):
    tasks = sett.pending + sett.done
    count = {"No Project": [0] * 3}
    for task in tasks:
        if len(task.project) == 0:
            count["No Project"][0] += 1
            if task.status is task.Status.DONE:
                count["No Project"][1] += 1
            count["No Project"][2] += task.get_age()
        for proj in task.project:
            if proj in count.keys():
                count[proj][0] += 1
                if task.status is task.Status.DONE:
                    count[proj][1] += 1
                count[proj][2] += task.get_age()
            else:
                count[proj] = [1, 0, task.get_age()]
                if task.status is task.Status.DONE:
                    count[proj][1] += 1
    count = [[x, y] for x, y in count.items()]
    for proj in count:
        proj[1][2] /= proj[1][0]
    new = []
    for proj in count:
        if args.all is True or proj[1][0] != proj[1][1]:
            new.append(proj)
    count = new
    data = [["Project", "Remaining", "Total", "Avg Age", "Complete",
             "0%                        100%"]]
    for proj in count:
        avg_age = str()
        if proj[1][2] < 60:
            avg_age += "{}s".format(proj[1][2])
        elif proj[1][2] < 3600:
            avg_age += "{}m".format(int(proj[1][2] / 60))
        elif proj[1][2] < 86400:
            avg_age += "{}h".format(int(proj[1][2] / 3600))
        elif proj[1][2] < 604800:
            avg_age += "{}d".format(int(proj[1][2] / 86400))
        elif proj[1][2] < 2628000:
            avg_age += "{}W".format(int(proj[1][2] / 604800))
        elif proj[1][2] < 31540000:
            avg_age += "{}M".format(int(proj[1][2] / 2628000))
        else:
            avg_age += "{}Y".format(int(proj[1][2] / 31540000))
        bar = str()
        for i in range(0, 30):
            if i <= int(30 * (proj[1][1] / proj[1][0])):
                bar += "\u2588"
            else:
                bar += " "
        bar = sett.theme.get_color(
            "report.summary.completed") + bar + sett.theme.reset()
        data.append([proj[0].title(), "{}".format(proj[1][0] - proj[1][1]),
                     "{}".format(proj[1][0]), avg_age, "{}".format(proj[1][1]), bar])
    table = Table()
    table.data = data
    table.flags['zebra'] = True
    table.flags['title_row'] = [0]
    table.title_fmt = ["\033[1;4m", "\033[21;24m"]
    table.fmt = table.BoxFormat.SPACE
    table.flags['vert_sep'] = True
    table.display()
    if reset is True:
        print('\033[{}F'.format(len(data)), end='')


def active(args, reset):
    has_print = False
    count = 0
    for task in sett.pending:
        if task.active is True:
            print("{}Task {} \'{}\' [{}]{}".format(
                sett.theme.get_color("start"), task.id, task.description,
                task.times[-1].print_duration(True), sett.theme.reset()))
            has_print = True
            count += 1
    if has_print is False:
        print("{}No active Tasks{}".format(
            sett.theme.get_color("start"), sett.theme.reset()))
        count += 1
    if reset is True:
        print('\033[{}F'.format(count), end='')


def times(args, reset):
    start, end = get_range(args)
    data = {}
    total = 0
    if args.group == 'all' or args.group == 'pending':
        for task in sett.pending:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        data[t.start.date()] = [0]
                    data[t.start.date()].append((task.description, t.print_start(
                        True), t.print_end(True), t.print_duration(True)))
                    data[t.start.date()][0] += t.get_duration()
                    total += t.get_duration()
    if args.group == 'all' or args.group == 'completed':
        for task in sett.done:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        data[t.start.date()] = [0]
                    data[t.start.date()].append((task.description, t.print_start(
                        True), t.print_end(True), t.print_duration(True)))
                    data[t.start.date()][0] += t.get_duration()
                    total += t.get_duration()
    data = sorted(list(data.items()), key=lambda x: x[0])
    display = [["Date/Description", "Start", "End", "Duration"]]
    table = Table()
    table.flags['title_row'] = [0]
    index = 1
    for a in data:
        display.append([a[0].strftime("%a %b %d, %Y"), '', '', ''])
        table.flags['title_row'].append(index)
        for b in a[1][1:]:
            display.append([b[0], b[1], b[2], b[3]])
            index += 1
        display.append(['', '', '', "{:02}:{:02}:{:02}".format(divmod(divmod(a[1][0], 60)[
                       0], 60)[0], divmod(divmod(a[1][0], 60)[0], 60)[1], divmod(a[1][0], 60)[1])])
        index += 2
    display.append(['', '', '', ''])
    display.append(['Total', '', '', "{:02}:{:02}:{:02}".format(divmod(divmod(total, 60)[
                   0], 60)[0], divmod(divmod(total, 60)[0], 60)[1], divmod(total, 60)[1])])
    table.flags['title_row'].append(index + 1)
    table.data = display
    table.update_alignment()
    table.col_align(0, 'r')
    table.row_align(table.flags['title_row'], 'l')
    table.flags['zebra'] = True
    table.title_fmt = ["\033[1;4m", "\033[21;24m"]
    table.fmt = table.BoxFormat.SPACE
    table.flags['vert_sep'] = True
    table.display()
    if reset is True:
        print('\033[{}F'.format(len(display)), end='')


def burndown(args, reset):
    start, end = get_range(args)
    if start.date() == end.date():
        start -= timedelta(7)
    if end.date() == datetime.now().date():
        end += timedelta(1)
    diff = (end.date() - start.date()).days
    data = {date: [0, 0, 0]
            for date in (start.date() + timedelta(n) for n in range(diff))}
    if end.date() >= datetime.now().date():
        end = datetime.now() + timedelta(1)
    height, width = os.popen('stty size', 'r').read().split()
    height = int(height)
    width = int(width)
    for task in sett.pending:
        if task.entry_date > end:
            continue
        if len(task.times) != 0:
            started = task.times[0].start
            if started < start:
                started = start
        else:
            started = datetime.now() + timedelta(1)
        if task.entry_date < start:
            entry = start
        else:
            entry = task.entry_date
        diff = (started.date() - entry.date()).days
        for date in (entry.date() + timedelta(n) for n in range(diff)):
            data[date] = [data[date][0] + 1, data[date][1], data[date][2]]
        diff = (end.date() - started.date()).days
        for date in (started.date() + timedelta(n) for n in range(diff)):
            data[date] = [data[date][0], data[date][1] + 1, data[date][2]]
    for task in sett.done:
        if task.entry_date > end:
            continue
        if task.entry_date < start:
            entry = start
        else:
            entry = task.entry_date
        if task.done_date < start:
            done = start
        else:
            done = task.done_date
        if len(task.times) != 0:
            started = task.times[0].start
            if started < start:
                started = start
        else:
            started = done
        diff = (started.date() - entry.date()).days
        for date in (entry.date() + timedelta(n) for n in range(diff)):
            data[date] = [data[date][0] + 1, data[date][1], data[date][2]]
        diff = (done.date() - started.date()).days
        for date in (started.date() + timedelta(n) for n in range(diff)):
            data[date] = [data[date][0], data[date][1] + 1, data[date][2]]
        diff = (end.date() - done.date()).days
        for date in (done.date() + timedelta(n) for n in range(diff)):
            data[date] = [data[date][0], data[date][1], data[date][2] + 1]
    max_count = 0
    for key, value in data.items():
        max_count = max(max_count, sum(value))
    if max_count > 10:
        max_count = int(math.ceil(max_count / 10.0)) * 10
    for key, value in data.items():
        data[key] = [value[0] / max_count, value[1] /
                     max_count, value[2] / max_count]
    data = sorted(list(data.items()), key=lambda x: x[0])
    if args.trim is True:
        tmp = list()
        store = 0
        for key, value in data:
            if store == 0 and value != [0, 0, 0]:
                store = 1
            if store == 1:
                tmp.append((key, value))
        store = 0
        data = tmp
        tmp = list()
        for key, value in reversed(data):
            if store == 0 and value != [0, 0, 0]:
                store = 1
            if store == 1:
                tmp.append((key, value))
        data = list(reversed(tmp))
    # TODO(Arden): Remove display requierment
    print(display.print_aligned(sett.theme.get_color('title') + start.strftime('%a %b %d, %Y') +
                                ' -- ' + end.strftime('%a %b %d, %Y') + sett.theme.reset(), 'c', width))
    print(' ' * 18, end='')
    if max_count > 10:
        wid = int((width - 18) / 4)
        for r in range(0, max_count, int(math.ceil(max_count / 40.0)) * 10):
            print("{:<{}}".format(r, wid - len(str(r))), end='')
        print(max_count)
    else:
        wid = int((width - 18) / max_count)
        for r in range(0, max_count):
            print("{:<{}}".format(r, wid - len(str(r))), end='')
        print(max_count)
    width -= 18
    for key, value in data:
        print(key.strftime("%a %b %d, %Y"), end='  ')
        print(sett.theme.get_color("reports.burndown.pending"), end='')
        print(' ' * int(width * value[0]), end='')
        print(sett.theme.get_color("reports.burndown.started"), end='')
        print(' ' * int(width * value[1]), end='')
        print(sett.theme.get_color("reports.burndown.done"), end='')
        print(' ' * int(width * value[2]), end='')
        print(sett.theme.reset())
    if reset is True:
        print('\033[{}F'.format(len(data) + 2), end='')


def graph(args, reset):
    hour_start = 0
    hour_end = 24
    if sett.in_data('settings.reports.graph.start'):
        hour_start = sett.get_data('settings.reports.graph.start')
    if sett.in_data('settings.reports.graph.end'):
        hour_end = sett.get_data('settings.reports.graph.end')
    hour_range = hour_end - hour_start
    start, end = get_range(args)
    height, width = os.popen('stty size', 'r').read().split()
    height = int(height)
    width = int(width)
    data = {}
    totals = {'total': 0}
    if args.group == 'all' or args.group == 'pending':
        for task in sett.pending:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        totals[t.start.date()] = 0
                        data[t.start.date()] = list()
                    totals[t.start.date()] += t.get_duration()
                    totals['total'] += t.get_duration()
                    if t.end is not None:
                        data[t.start.date()].append(
                            ((task.description, task.project), t.start, t.end))
                    else:
                        data[t.start.date()].append(
                            ((task.description, task.project), t.start, datetime.now()))
    if args.group == 'all' or args.group == 'completed':
        for task in sett.done:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        totals[t.start.date()] = 0
                        data[t.start.date()] = list()
                    totals[t.start.date()] += t.get_duration()
                    totals['total'] += t.get_duration()
                    if t.end is not None:
                        data[t.start.date()].append(
                            ((task.description, task.project), t.start, t.end))
                    else:
                        data[t.start.date()].append(
                            ((task.description, task.project), t.start, datetime.now()))
    for x in data:
        data[x] = sorted(data[x], key=lambda x: x[1])
    if args.trim_all is False:
        day_count = (end - start).days
        for date in (start + timedelta(n) for n in range(day_count)):
            if date.date() not in data:
                data[date.date()] = []
    data = sorted(list(data.items()), key=lambda x: x[0])
    if args.trim is True:
        tmp = list()
        store = 0
        for key, value in data:
            if store == 0 and len(value) != 0:
                store = 1
            if store == 1:
                tmp.append((key, value))
        store = 0
        data = tmp
        tmp = list()
        for key, value in reversed(data):
            if store == 0 and len(value) != 0:
                store = 1
            if store == 1:
                tmp.append((key, value))
        data = reversed(tmp)
    if start.date() == end.date():
        #TODO
        print(display.print_aligned(sett.theme.get_color('title') +
                                    start.strftime('%a %b %d, %Y') + sett.theme.reset(), 'c', width))
        hour = (width - 7) / hour_range
    else:
        #TODO
        print(display.print_aligned(sett.theme.get_color('title') + start.strftime('%a %b %d, %Y') +
                                    ' -- ' + end.strftime('%a %b %d, %Y') + sett.theme.reset(), 'c', width))
        hour = (width - 18) / hour_range
        print(' ' * 11, end='')
    for i in range(hour_start, hour_end):
        print("{:<{}}".format(str(i) + ":00", int(hour)), end='')
    print()
    colors = {}
    rem_col = list(range(255))[17:-25]
    for key, value in data:
        if start.date() != end.date():
            print(key.strftime('%d-%m-%Y'), end=' ')
        current = datetime.combine(
            key, datetime.min.time()).replace(hour=hour_start)
        day_end = datetime.combine(key, datetime.max.time())
        step = (3600 * hour_range) / (int(hour) * hour_range)
        index = 0
        active = 0
        char_index = 0
        while current <= day_end:
            if len(value) == 0:
                active = 4
            if active == 0 and current > value[index][1]:
                color_ref = value[index][0][0]
                if value[index][0][1] != list():
                    color_ref = value[index][0][1][0]
                if color_ref not in colors:
                    if len(colors) < 15:
                        colors[color_ref] = len(colors) + 1
                    else:
                        if len(rem_col) == 0:
                            rem_col = list(range(255))[17:-25]
                        colors[color_ref] = random.choice(rem_col)
                        rem_col.remove(colors[color_ref])
                #TODO
                print(sett.theme.get_color_escape(colors[color_ref], True), end='')
                char_index = 0
                active = 1
            if (active in (1, 2, 3)) and current > value[index][2]:
                print(sett.theme.reset(), end='')
                active = 0
                if len(value) > index + 1:
                    index += 1
                else:
                    active = 4
            if current.date() == datetime.today().date() and current > datetime.now() and current - timedelta(seconds=step) < datetime.now():
                print(sett.theme.get_color("reports.graph.active") +
                      "\u2503" + sett.theme.reset(), end='')
            elif active == 2 or active == 0 or active == 4:
                print(' ', end='')
            elif active == 1:
                print(value[index][0][0][char_index], end='')
                char_index += 1
                if len(value[index][0][0]) == char_index and len(value[index][0][1]) == 0:
                    active = 2
                elif len(value[index][0][0]) == char_index:
                    char_index = 0
                    active = 3
            elif active == 3:
                print(("(" + value[index][0][1][0] + ")")[char_index], end='')
                char_index += 1
                if char_index == len(value[index][0][1][0]) + 2:
                    active = 2
            current += timedelta(seconds=step)
        print('\033[0m', end=' ')
        if day_end.date() in totals:
            print("{:02}:{:02}".format(divmod(divmod(totals[day_end.date()], 60)[0], 60)[
                  0], divmod(divmod(totals[day_end.date()], 60)[0], 60)[1]))
        else:
            print("00:00")
    total = end.date() - start.date()
    if total.days == 0:
        total = 86400
    else:
        total = total.days * 86400
    diff = total - totals['total']
    if start.date() != end.date():
        print(' ' * 10, end='')
    print(' ' * (int(hour) * hour_range), '\033[4m      \033[24m')
    if start.date() != end.date():
        print(' ' * 10, end='')
    print(' ' * (int(hour) * hour_range), "{:3}:{:02}".format(divmod(divmod(
        totals['total'], 60)[0], 60)[0], divmod(divmod(totals['total'], 60)[0], 60)[1]))
    if start.date() != end.date():
        print(' ' * 10, end='')
    print("Tracked:   {:>15}".format("{}:{:02}:{:02}".format(divmod(divmod(totals['total'], 60)[
          0], 60)[0], divmod(divmod(totals['total'], 60)[0], 60)[1], divmod(totals['total'], 60)[1])))
    if start.date() != end.date():
        print(' ' * 10, end='')
    print("Available: {:>15}".format("{}:{:02}:{:02}".format(divmod(divmod(diff, 60)[
          0], 60)[0], divmod(divmod(diff, 60)[0], 60)[1], divmod(diff, 60)[1])))
    if start.date() != end.date():
        print(' ' * 10, end='')
    print("Total:     {:>15}".format("{}:{:02}:{:02}".format(divmod(divmod(total, 60)[
          0], 60)[0], divmod(divmod(total, 60)[0], 60)[1], divmod(total, 60)[1])))
    print()
    if reset is True:
        print('\033[{}F'.format(len(data) + 8), end='')


def daterange(start_date, end_date, inc='day'):
    if inc == 'day':
        for n in range((end_date - start_date).days + 1):
            yield start_date + timedelta(n)
    elif inc == 'month':
        start_ym = 12 * start_date.year + start_date.month - 1
        end_ym = 12 * end_date.year + end_date.month - 1
        for ym in range(start_ym, end_ym):
            yield datetime(year=divmod(ym, 12)[0], month=divmod(ym, 12)[1] + 1, day=1)


def cal(args, reset):
    if args.start is None:
        args.start = datetime.now()
    if args.stop is None:
        args.stop = datetime.now().replace(day=calendar.monthrange(datetime.now().year, args.start.month + 1)[1], month=(args.start.month + 1) % 12)
    else:
        year_up = ((args.stop.month+1)%12)
        if year_up != 1:
            year_up = 0
        args.stop = args.stop.replace(month=(args.stop.month + 1) % 12, year=args.stop.year + year_up, day=calendar.monthrange(args.stop.year, args.stop.month)[1] - 1)
    data = {}
    for task in sett.pending:
        if task.due_date is not None:
            if task.is_overdue() is True:
                if task.due_date.date() in data:
                    data[task.due_date.date()] = min(data[task.due_date.date()], 1)
                else:
                    data[task.due_date.date()] = 1
            elif task.due_today() is True:
                if task.due_date.date() in data:
                    data[task.due_date.date()] = min(data[task.due_date.date()], 2)
                else:
                    data[task.due_date.date()] = 2
            else:
                if task.due_date.date() in data:
                    data[task.due_date.date()] = min(data[task.due_date.date()], -(int(task.urgency) - 13))
                else:
                    data[task.due_date.date()] = -(int(task.urgency) - 13)
    mon_count = sum(1 for _ in daterange(args.start, args.stop, 'month'))
    width = 20
    if mon_count >= 3:
        width = 64
    elif mon_count == 2:
        width = 42
    year = 0
    index = 0
    for month in daterange(args.start, args.stop, 'month'):
        if month.year != year:
            year = month.year
            #TODO
            print(display.print_aligned(sett.theme.get_color('title') + "  {}  ".format(year) + sett.theme.reset(), 'c', width))
        lines = 4
        indent = 0
        if index % 3 == 1:
            indent = 22
        elif index % 3 == 2:
            indent = 44
        days = calendar.monthrange(month.year, month.month)[1]
        dow = (month.replace(day=1).weekday() + 1) % 7
        if indent != 0:
            print("\033[G\033[{}C{:^20}".format(indent, month.strftime("%B %Y")))
            print("\033[G\033[{}CSu Mo Tu We Th Fr Sa".format(indent))
        else:
            print("{:^20}".format(month.strftime("%B %Y")))
            print("Su Mo Tu We Th Fr Sa")
        for dt in daterange(month, month.replace(day=calendar.monthrange(month.year, month.month)[1])):
            space = (dt.weekday() + 1) % 7
            if dt.date() == datetime.now().date() and dt.date() not in data:
                print(sett.theme.get_color('reports.calendar.active'), end='')
            if space == 0 or space == 6:
                print(sett.theme.get_color('reports.calendar.weekend'), end='')
            if dt.date() in data:
                if data[dt.date()] == 1:
                    print(sett.theme.get_color('reports.calendar.overdue'), end='')
                elif data[dt.date()] == 2:
                    print(sett.theme.get_color('reports.calendar.due_today'), end='')
                else:
                    print(sett.theme.get_color('reports.calendar.urg{}'.format(13 - data[dt.date()])), end='')
            if space != 0 or indent != 0:
                print("\033[G\033[{}C{:2}".format((3 * space) + indent, dt.day), end='')
            else:
                print("{:2}".format(dt.day), end='')
            if dt.date() in data or space in (0, 6) or dt.date() == datetime.now().date():
                print(sett.theme.reset(), end='')
            if space == 6:
                print()
                lines += 1
        print()
        if index != mon_count - 1:
            print("\033[{}F".format(lines))
        index += 1
        if index % 3 == 0 and index != mon_count:
            print("\n" * 9, end='')


def get_range(args):
    if args.start is None:
        start = datetime.now().replace(hour=0, minute=0, second=0)
    else:
        start = args.start[1]
    if args.stop is None and args.start is not None:
        end = datetime.now().replace(hour=23, minute=59, second=59)
        if args.start[0] == 'yesterday':
            end -= timedelta(days=1)
        elif args.start[0] == 'week':
            end = start + timedelta(days=7)
        elif args.start[0] == 'lastweek':
            end = start + timedelta(days=7)
        elif args.start[0] == 'month':
            end = start + \
                timedelta(days=calendar.monthrange(start.year, start.month)[1])
        elif args.start[0] == 'lastmonth':
            end = start + \
                timedelta(days=calendar.monthrange(start.year, start.month)[1])
        elif args.start[0] == 'year':
            end = start.replace(month=12, day=31)
        elif args.start[0] == 'lastyear':
            end = start.replace(month=12, day=31)
    elif args.stop is None and args.start is None:
        end = datetime.now().replace(hour=23, minute=59, second=59)
    else:
        end = args.stop[1]
        if end.hour == 0 and end.minute == 0 and end.second == 0:
            end = end.replace(hour=23, minute=59, second=59)
    return start, end
