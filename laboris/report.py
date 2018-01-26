import time
import calendar
import os
import laboris.settings as sett
import laboris.printer as printer

from ioterm.table import Table
import ioterm.display as display
import ioterm.color as color
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



def summary(args, reset):
    tasks = sett._pending + sett._done
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
        bar = sett._theme.get_color(
            "report.summary.completed") + bar + sett._theme.reset()
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
    for task in sett._pending:
        if task.active is True:
            print("{}Task {} \'{}\' [{}]{}".format(
                sett._theme.get_color("start"), task.id, task.description,
                task.times[-1].print_duration(True), sett._theme.reset()))
            has_print = True
            count += 1
    if has_print is False:
        print("{}No active Tasks{}".format(
            sett._theme.get_color("start"), sett._theme.reset()))
        count += 1
    if reset is True:
        print('\033[{}F'.format(count), end='')


def times(args, reset):
    start, end = get_range(args)
    data = {}
    total = 0
    if args.group == 'all' or args.group == 'pending':
        for task in sett._pending:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        data[t.start.date()] = [0]
                    data[t.start.date()].append((task.description, t.print_start(
                        True), t.print_end(True), t.print_duration(True)))
                    data[t.start.date()][0] += t.get_duration()
                    total += t.get_duration()
    if args.group == 'all' or args.group == 'completed':
        for task in sett._done:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        data[t.start.date()] = [0]
                    data[t.start.date()].append((task.description, t.print_start(
                        True), t.print_end(True), t.print_duration(True)))
                    data[t.start.date()][0] += t.get_duration()
                    total += t.get_duration()
    from pprint import pprint
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
    pass

def graph(args, reset):
    start, end = get_range(args)
    height, width = os.popen('stty size', 'r').read().split()
    height = int(height)
    width = int(width)
    data = {}
    total = 0
    if args.group == 'all' or args.group == 'pending':
        for task in sett._pending:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        data[t.start.date()] = list()
                    if t.end is not None:
                        data[t.start.date()].append(((task.description, task.project), t.start, t.end))
                    else:
                        data[t.start.date()].append(((task.description, task.project), t.start, datetime.now()))
                    total += t.get_duration()
    if args.group == 'all' or args.group == 'completed':
        for task in sett._done:
            for t in task.times:
                if t.start > start and t.start <= end:
                    if t.start.date() not in data:
                        data[t.start.date()] = list()
                    if t.end is not None:
                        data[t.start.date()].append(((task.description, task.project), t.start, t.end))
                    else:
                        data[t.start.date()].append(((task.description, task.project), t.start, datetime.now()))
                    total += t.get_duration()
    from pprint import pprint
    for x in data:
        data[x] = sorted(data[x], key=lambda x: x[1])
    if start.date() == end.date():
        print(display.print_aligned(sett._theme.get_color('title') + start.strftime('%a %b %d, %Y') + sett._theme.reset(), 'c', width))
        hour = width / 24.0
    else:
        print(display.print_aligned(sett._theme.get_color('title') + start.strftime('%a %b %d, %Y') + ' -- ' + end.strftime('%a %b %d, %Y') + sett._theme.reset(), 'c', width))
        hour = (width - 11) / 24.0
        print(' ' * 11, end='')
    for i in range(24):
        print("{:<{}}".format(str(i) + ":00", int(hour)), end='')
    print()
    data = sorted(list(data.items()), key=lambda x: x[0])
    colors = {}
    rem_col = list(range(255))
    for key, value in data:
        print(key.strftime('%d-%m-%Y'), end=' ')
        current = datetime.combine(key, datetime.min.time())
        day_end = datetime.combine(key, datetime.max.time())
        step = 86400 / (int(hour) * 24.0)
        index = 0
        active = 0
        while current <= day_end:
            if current > value[index][1] and active is 0:
                if value[index][0][1] != list():
                    if len(colors) <= 15:
                        colors[value[index][0][1][0]] = len(colors) + 1
                    else:
                        colors[value[index][0][1][0]] = random.choice(rem_col)
                        print(color.get_color(colors[value[index][0][1][0]]),end='')
                else:
                    if len(colors) <= 15:
                        colors[value[index][0][0]] = len(colors) + 1
                    else:
                        colors[value[index][0][0]] = random.choice(rem_col)
                    print(color.get_color(colors[value[index][0][0]]),end='')
                print(value[index][0], end='')
                active = 1
            if current > value[index][2] and active is 1:
                print("\033[0m", end='')
                active = 0
                if len(value) > index + 1:
                    index += 1
                else:
                    active = 2
            print(' ', end='')
            current += timedelta(seconds=step)
        print('\033[0m')
    print(data)
    print()
    print(colors)
    print()
    print(rem_col)



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
