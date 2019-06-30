import laboris.config as cfg
import laboris.data as dat

import datetime

def ilen(string):
    length = 0
    counting = True
    for ch in string:
        if ch == '\033' or ch == '\x1b':
            counting = False
        elif not counting and ch == 'm':
            counting = True
        elif counting:
            length += 1
    return length

def dlen(string, min_width):
    length = 0
    counting = True
    for ch in string:
        if ch == '\033':
            counting = False
        elif counting and ch == 'm':
            counting = True
        else:
            length += 1
    return min_width + len(string) - length

def date_abbrev(lhs, rhs):
    if not rhs or rhs <= 0:
        return ""
    output = ""
    if isinstance(lhs, int):
        lhs = datetime.datetime.fromtimestamp(lhs)
    if isinstance(rhs, int):
        rhs = datetime.datetime.fromtimestamp(rhs)
    if rhs is None:
        return output
    if lhs > rhs:
        diff = lhs - rhs
        output += '-'
    else:
        diff = rhs - lhs
    if abs(diff.days) > 7:
        output += str(int(diff.days / 7)) + "w"
    elif abs(diff.days) > 0:
        output += str(int(diff.days)) + 'd'
    elif abs(diff.seconds) > 3600:
        output += str(int(diff.seconds / 3600)) + "h"
    elif abs(diff.seconds) > 60:
        output += str(int(diff.seconds / 60)) + "m"
    elif abs(diff.seconds) > 0:
        output += str(diff.seconds) + "s"
    else:
        output = "NOW"
    return output

def print_task(task):
    task_color = cfg.get_urg(task['urg'])
    if 'dueDate' in task and task['dueDate'] and datetime.datetime.fromtimestamp(task['dueDate']).date() == datetime.datetime.now().date():
        task_color = cfg.CONFIG['theme']['staDueToday']
    elif 'dueDate' in task and task['dueDate'] and datetime.datetime.fromtimestamp(task['dueDate']).date() < datetime.datetime.now().date():
        task_color = cfg.CONFIG['theme']['staOverdue']
    elif 'times' in task and task['times'] and len(task['times'][-1]) == 1:
        task_color = cfg.CONFIG['theme']['staActive']
    res = "\033[0;1m{}\033[0m {}{}\033[0m".format(task['uuid'][:4], task_color, task['title'])
    res += (cfg.CONFIG['theme']['project'] + " +" + " +".join(task['projects']) + "\033[0m" if task['projects'] else '')
    res += (cfg.CONFIG['theme']['tag'] + " @" + " @".join(task['tags']) + "\033[0m" if task['tags'] else '')
    return res

def fmt_duration(time):
    hour = 0
    minute = 0
    minute = time // 60
    time -= (minute * 60)
    hour = minute // 60
    minute -= (hour * 60)
    return "{:3}:{:02}:{:02}".format(hour, minute, time)

def fmt_time(time):
    return datetime.datetime.fromtimestamp(time).strftime("%H:%M:%S")
