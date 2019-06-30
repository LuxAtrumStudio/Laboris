import laboris.config as cfg
import laboris.data as dat
from laboris.reports.util import *

import datetime

def calc_time_data(task):
    today = int(datetime.datetime.today().replace(hour=0,minute=0,second=0).timestamp())
    seven = int((datetime.datetime.today() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0).timestamp())
    if not task['times']:
        return None
    stoday = 0
    sseven = 0
    total = 0
    for interval in task['times']:
        if len(interval) == 1:
            interval = [interval[0], int(datetime.datetime.now().timestamp())]
        if interval[0] > today:
            stoday += (interval[1] - interval[0])
            sseven += (interval[1] - interval[0])
            total += (interval[1] - interval[0])
        elif interval[0] > seven:
            sseven += (interval[1] - interval[0])
            total += (interval[1] - interval[0])
        else:
            total += (interval[1] - interval[0])
    return (stoday, sseven, total)

def print_daily_times(task, line, padding):
    if not task['times']:
        return line
    times = {}
    for interval in task['times']:
        if len(interval) == 1:
            interval = [interval[0], int(datetime.datetime.now().timestamp())]
        day = datetime.datetime.fromtimestamp(interval[0]).strftime("%Y-%m-%d")
        if day in times:
            times[day] += (interval[1] - interval[0])
        else:
            times[day] = (interval[1] - interval[0])
    for day, duration in times.items():
        if line % 2 == 1:
            print("{}{}  {:<{}}\033[0m".format(cfg.CONFIG['theme']['bg'], " " * padding[0], "{}  {}".format(day, fmt_duration(duration)), padding[1]))
        else:
            print("{}  {:<{}}\033[0m".format(" " * padding[0], "{}  {}".format(day, fmt_duration(duration)), padding[1]))
        line += 1
    return line

def print_inter_times(task, line, padding):
    if not task['times']:
        return line
    times = {}
    for interval in task['times']:
        if len(interval) == 1:
            interval = [interval[0], int(datetime.datetime.now().timestamp())]
        day = datetime.datetime.fromtimestamp(interval[0]).strftime("%Y-%m-%d")
        if day in times:
            times[day].append([interval[0], interval[1], (interval[1] - interval[0])])
        else:
            times[day] = [[interval[0], interval[1], (interval[1] - interval[0])]]
    for day, entries in times.items():
        if line % 2 == 1:
            print('{}{} {:<{}}\033[0m'.format(cfg.CONFIG['theme']['bg'], " " * padding[0], day, padding[1]))
        else:
            print('{} {:<{}}\033[0m'.format(" " * padding[0], day, padding[1]))
        line += 1
        for entry in entries:
            if line % 2 == 1:
                print('{}{}    {:<{}}\033[0m'.format(cfg.CONFIG['theme']['bg'], " " * padding[0], "{}-{} [{}]".format(fmt_time(entry[0]), fmt_time(entry[1]), fmt_duration(entry[2])), padding[1] - 3))
            else:
                print('{}    {:<{}}\033[0m'.format(" " * padding[0], "{}-{} [{}]".format(fmt_time(entry[0]), fmt_time(entry[1]), fmt_duration(entry[2])), padding[1] - 3))
            line += 1
    return line

def main(args):
    idx = dat.find(args['task'])
    task = dat.DATA[0][idx] if idx >= 0 else dat.DATA[1][-idx-1]
    time_data = calc_time_data(task)
    if 'urg' not in task:
        task['urg'] = 0.0
    data = [
            ("Title", "{}{}".format(cfg.get_urg(task['urg']), task['title'])),
            ("Projects", (cfg.CONFIG['theme']['project'] + ' '.join(task['projects']) if task['projects'] else None)),
            ("Tags", (cfg.CONFIG['theme']['tag'] + ' '.join(task['tags']) if task['tags'] else None)),
            ("Due Date", (datetime.datetime.fromtimestamp(task['dueDate']).strftime("%Y-%m-%d %H:%M:%S") if task['dueDate'] else None)),
            ("Urgency", "{}{:.5}".format(cfg.get_urg(task['urg']), task['urg'])),
            ("", "Age:      {:.5}".format(abs(0.01429 * dat.datediff(datetime.datetime.fromtimestamp(task['entryDate']), datetime.datetime.now())))),
            ("", ("Due:      {:.5}".format(abs(9.0 * dat.urgdue(task))) if task['dueDate'] else None)),
            ("", "Project:  {:.5}".format(abs(1.0 * len(task['projects'])))),
            ("", "Tag:      {:.5}".format(abs(1.0 * len(task['tags'])))),
            ("Priority", str(task['priority'])),
            ("Time Today", (fmt_duration(time_data[0]) if time_data else None)),
            ("Time 7 Days", (fmt_duration(time_data[1]) if time_data else None)),
            ("Time Total", (fmt_duration(time_data[2]) if time_data else None)),
            ("UUID", task['uuid']),
            ("Entry Date", datetime.datetime.fromtimestamp(task['entryDate']).strftime("%Y-%m-%d %H:%M:%S")),
            ("Done Date", (datetime.datetime.fromtimestamp(task['doneDate']).strftime("%Y-%m-%d %H:%M:%S") if 'doneDate' in task and task['doneDate'] else None)),
            ("Modified Date", datetime.datetime.fromtimestamp(task['modifiedDate']).strftime("%Y-%m-%d %H:%M:%S")),
            ("Status", task['status']),
            ("Times", (" " * 20 if task['times'] else None))
            ]
    padding = [3, 5]
    for key, value in data:
        padding[0] = max(padding[0], ilen(str(key)))
        padding[1] = max(padding[1], ilen(str(value)))
    print(print_task(task))
    print("{}{:{}}\033[0m  {}{:{}}\033[0m".format(cfg.CONFIG['theme']['title'], "Key", padding[0], cfg.CONFIG['theme']['title'], "Value", padding[1]))
    line = 0
    for key, value in data:
        if value is not None:
            if line % 2 == 1:
                print("{}{:{}}  {}\033[0m".format(cfg.CONFIG['theme']['bg'], key, padding[0], value + (" " * (padding[1] - ilen(value)))))
            else:
                print("{:{}}  {}\033[0m".format(key, padding[0], value + (" " * (padding[1] - ilen(value)))))
            line += 1
    print_inter_times(task, line, padding)
    # print_daily_times(task, line, padding)
