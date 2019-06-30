import laboris.config as cfg
import laboris.data as dat
from laboris.reports.util import *

import datetime

def print_entry(task, fmt, ind, spacing):
    data = task
    data['suuid'] = data['uuid'][:8]
    data['due'] = date_abbrev(datetime.datetime.now(), task['dueDate'] if 'dueDate' in task else -1)
    data['title'] = "{:{}}".format(task['title'], spacing[0])
    data['projects'] = "{:{}}".format(" ".join(task['projects']), spacing[1])
    data['tags'] = "{:{}}".format(" ".join(task['tags']), spacing[2])
    data['p'] = ' ' if task['priority'] == -1 else task['priority']
    data['urg'] = data['urg'] if 'urg' in data else 0
    print("{}{}{}\033[0m".format("" if ind % 2 == 1 else cfg.CONFIG['theme']['bg'], cfg.get_urg(data['urg']),
          fmt.format(data)))


def main(args):
    fmt = "{0[id]:2} {0[p]:1} {0[due]:>3} {0[title]} {0[projects]} {0[tags]} {0[urg]:6.3f}"
    if 'all' in args and args['all']:
        fmt = "{0[suuid]:4} {0[title]} {0[projects]} {0[tags]}"
    if 'fmt' in args:
        fmt = args.fmt
    spacing = [5, 8, 4]
    for task in dat.DATA[0]:
        spacing[0] = max(spacing[0], len(task['title']))
        spacing[1] = max(spacing[1], len(" ".join(task['projects'])))
        spacing[2] = max(spacing[2], len(" ".join(task['tags'])))
        if task['times'] and len(task['times'][-1]) == 1:
            print(print_task(task))
        elif 'dueDate' in task and task['dueDate'] and datetime.datetime.fromtimestamp(
                task['dueDate']).date() <= datetime.datetime.now().date():
            print(print_task(task))
    if 'all' in args and args['all']:
        for task in dat.DATA[1]:
            spacing[0] = max(spacing[0], len(task['title']))
            spacing[1] = max(spacing[1], len(" ".join(task['projects'])))
            spacing[2] = max(spacing[2], len(" ".join(task['tags'])))
    data = {
        'id': "ID",
        'uuid': "UUID                            ",
        'suuid': "UUID    ",
        'p': "P",
        'age': "Age",
        'due': "Due",
        'dueShort': "Due",
        'title': "{:{}}".format("Title", spacing[0]),
        'projects': "{:{}}".format("Projects", spacing[1]),
        'tags': "{:{}}".format("Tags", spacing[2]),
        'urg': "Urg",
    }
    tmp_fmt = fmt.replace('{', cfg.CONFIG['theme']['title'] + '{')
    tmp_fmt = tmp_fmt.replace('}', '}\033[0m')
    tmp_fmt = tmp_fmt.replace('f}', '}')
    print(tmp_fmt.format(data))
    for i, task in enumerate(dat.DATA[0]):
        print_entry(task, fmt, i, spacing)
    if 'all' in args and args['all']:
        for i, task in enumerate(dat.DATA[1]):
            print_entry(task, fmt, i, spacing)


def detail(args):
    task = dat.find(args['task'])
