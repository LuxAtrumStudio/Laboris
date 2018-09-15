import datetime
import laboris.task
from laboris.color import Attr, GetAttr, Color, NoReset
from laboris.config import CONFIG

def disp_length(string, min_width):
    string = str(string)
    counting = False
    count = 0
    for ch in string:
        if ch == '\033':
            counting = True
        elif ch == 'm' and counting:
            counting = False
        elif counting is False:
            count += 1
    return min_width + len(string) - count

def get_diff(start, end):
    seconds = end - start
    minutes = 0
    hours = 0
    minutes = seconds // 60
    seconds -= minutes * 60
    hours = minutes // 60
    minutes -= hours * 60
    return "{:02}:{:02}".format(hours, minutes)

def get_total(times):
    sec = 0
    for start, stop in times:
        sec += (stop - start)
    minutes = sec // 60
    sec -= minutes * 60
    hours = minutes // 60
    minutes -= hours * 60
    return "{:02}:{:02}".format(hours, minutes)


def detail_action(task, args):
    task = laboris.task.get_uuid(task[1])
    data = {
        "Title": NoReset(task['title'], CONFIG.get_color('urgency', task['urg'])),
        'Projects': NoReset(' '.join(task['projects']), CONFIG.get_color('comp.project')) if task['projects'] else None,
        'Tags': NoReset(' '.join(task['tags']), CONFIG.get_color('comp.tag')) if task['tags'] else None,
        'Urg': NoReset('{:5.3f}'.format(task['urg']), CONFIG.get_color('urgency', task['urg'])),
        "Id": task['id'] if 'id' in task else None,
        'Uuid': task['uuid'],
        'Priority': 0 if task['priority'] == -1 else task['priority'],
        'Status': 'Pending' if task['status'] == "PENDING" else 'Completed',
        'Entry Date': datetime.datetime.fromtimestamp( task['entryDate']).strftime("%d-%m-%Y %H:%M:%S"),
        'Due Date': datetime.datetime.fromtimestamp( task['dueDate']).strftime("%d-%m-%Y %H:%M:%S") if task['dueDate'] else None,
        'Done Date': datetime.datetime.fromtimestamp( task['doneDate']).strftime("%d-%m-%Y %H:%M:%S") if task['doneDate'] else None,
        'Modified Date': datetime.datetime.fromtimestamp( task['modifiedDate']).strftime("%d-%m-%Y %H:%M:%S") if task['modifiedDate'] else None,
        'Times:': '' if task['times'] else None
    }
    key_width= len('Key')
    value_width = len('Value')
    for key, value in data.items():
        key_width = max(key_width, len(str(key)))
        value_width = max(value_width, len(str(value)))
    print(Attr("{:{}}".format("Key", key_width), CONFIG.get_color('title')), Attr("{:{}}".format("Value", value_width), CONFIG.get_color('title')))
    line = 0
    for key, value in data.items():
        if value is not None:
            if line % 2 == 1:
                print(Attr("{} {:<{}}".format("\033[1m{:{}}\033[21m".format(key, key_width), value, disp_length(value, value_width)), CONFIG.get_color('background'), bg=True))
            else:
                print("{} {:<{}}\033[0m".format(Attr("{:{}}".format(key, key_width), 'bold'), value, value_width))
            line += 1
    if task['times']:
        for start, stop in task['times']:
            fmt = "{} - {}   {}".format(datetime.datetime.fromtimestamp(start).strftime("%d-%m %H:%M"), datetime.datetime.fromtimestamp(stop).strftime("%d-%m %H:%M"), get_diff(start, stop))
            if line % 2 == 1:
                print(Attr("{:>{}}".format(fmt, key_width + 1 + value_width), CONFIG.get_color('background'), bg=True))
            else:
                print("{:>{}}".format(fmt, key_width + 1 + value_width))
            line += 1
        print("\033[1m{:<{}} {:<{}}".format('Total', key_width, get_total(task['times']), value_width))

