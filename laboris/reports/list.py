import laboris.config as cfg
import laboris.data as dat

import datetime


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
    pass


def print_entry(task, fmt, ind, spacing):
    data = {'id': ind, **task}
    data['due'] = date_abbrev(datetime.datetime.now, task['dueDate'] if 'dueDate' in task else -1)
    data['title'] = "{:{}}".format(task['title'], spacing[0])
    data['projects'] = "{:{}}".format(" ".join(task['projects']), spacing[1])
    data['tags'] = "{:{}}".format(" ".join(task['tags']), spacing[2])
    data['p'] = task['priority']
    print("{}{}{}\033[0m".format("" if ind % 2 == 1 else cfg.CONFIG['theme']['bg'], cfg.get_urg(data['urg']),
          fmt.format(data)))


def status(args):
    fmt = "{0[id]:2} {0[p]:1} {0[due]:>3} {0[title]} {0[projects]} {0[tags]} {0[urg]:6.3f}"
    if 'fmt' in args:
        fmt = args.fmt
    spacing = [5, 8, 4]
    for task in dat.DATA[0]:
        spacing[0] = max(spacing[0], len(task['title']))
        spacing[1] = max(spacing[1], len(" ".join(task['projects'])))
        spacing[2] = max(spacing[2], len(" ".join(task['tags'])))
        if task['times'] and len(task['times'][-1]) == 1:
            print_task(task)
        elif 'dueDate' in task and task['dueDate'] and datetime.datetime.fromtimestamp(
                task['dueDate']).date() <= datetime.datetime.now().date():
            print_task(task)
    data = {
        'id': "ID",
        'uuid': "UUID",
        'p': "P",
        'age': "Age",
        'due': "Due",
        'dueShort': "Due",
        'title': "{:{}}".format("Title", spacing[0]),
        'projects': "{:{}}".format("Projects", spacing[1]),
        'tags': "{:{}}".format("Tags", spacing[2]),
        'urg': "Urg"
    }
    tmp_fmt = fmt.replace('{', cfg.CONFIG['theme']['title'] + '{')
    tmp_fmt = tmp_fmt.replace('}', '}\033[0m')
    tmp_fmt = tmp_fmt.replace('f}', '}')
    print(tmp_fmt.format(data))
    for i, task in enumerate(dat.DATA[0]):
        print_entry(task, fmt, i, spacing)

def detail(args):
    task = dat.find(args.task)
