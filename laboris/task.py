"""
Task query system
"""

import os
import json
import datetime
from math import exp, log

from laboris.color import Attr
from laboris.config import CONFIG
import laboris.prompt as prompt

PENDING = {}
PENDING_ID = []
COMPLETED = {}
COMPLETED_ID = []

PENDING_FILE = "pending.json"


def date_diff(start, end):
    diff = start - end
    return diff.days + (diff.seconds / 86400)

# Double S Curve?
# =============================================================================
# def urgency_due(task):
#     if task['dueDate'] is None:
#         return 0.0
#     due = date_diff(datetime.datetime.now(),
#                     datetime.datetime.fromtimestamp(task['dueDate']))

# Linear?
# =============================================================================
# def urgency_due(task):
#     if task['dueDate'] is None:
#         return 0.0
#     due = date_diff(datetime.datetime.now(), datetime.datetime.fromtimestamp(task['dueDate']))
#     if due < -4:
#         return 0.2
#     else:
#         return 0.25*due+1.2

# Single S Curve?
# =============================================================================
def urgency_due(task):
    if task['dueDate'] is None:
        return 0.0
    due = date_diff(datetime.datetime.now(),
                    datetime.datetime.fromtimestamp(task['dueDate']))
    k = 0.7
    x0=-3.98677299562
    alpha = -5.966
    if due < alpha:
        return 0.2
    else:
        return 1.0 / (1 + exp(-k * (due - x0)))

# Single S Curve?
# =============================================================================
# def urgency_due(task):
#     if task['dueDate'] is None:
#         return 0.0
#     due = date_diff(datetime.datetime.now(),
#                     datetime.datetime.fromtimestamp(task['dueDate']))
#     k = 1
#     x0=-5
#     return 1.0 / (1 + exp(-k * (due - x0)))




def calc_urg(task):
    urg = 0.0
    urg += abs(0.01429 * date_diff(
        datetime.datetime.fromtimestamp(task['entryDate']),
                                        datetime.datetime.now()))
    urg += abs(9.0000 * urgency_due(task))
    urg += abs(1.00000 * len(task['projects']))
    urg += abs(0.20000 * len(task['tags']))
    urg += abs(1.00000 * task['priority'])
    urg += abs(4.0 if task['times'] and len(task['times'][-1]) == 1 else 0.0)
    if task['status'] == 'COMPLETED' or task['priority'] == -1:
        urg = 0.0
    return urg


# def urgency_due(task):
#     if task['dueDate'] is None:
#         return 0.0
#     late = False
#     if datetime.datetime.now() > datetime.datetime.fromtimestamp(
#             task['dueDate']):
#         diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(
#             task['dueDate'])
#         late = True
#     else:
#         diff = datetime.datetime.fromtimestamp(
#             task['dueDate']) - datetime.datetime.now()
#     overdue = diff.days + (diff.seconds / 86400)
#     if late is False:
#         overdue *= -1
#     if overdue > 7:
#         return 1.0
#     elif overdue >= -14:
#         return float((overdue + 14.0) * 0.8 / 21.0) + 0.2
#     return 0.2

# def calc_urg(task):
#     urg = 0.0
#     urg += abs(2.00 * urgency_age(task))
#     urg += abs(12.0 * urgency_due(task))
#     urg += abs(1.00 * task['priority'])
#     urg += abs(0.20 * len(task['tags']))
#     urg += abs(1.00 * len(task['projects']))
#     urg += abs(4.0 if task['times'] and len(task['times'][-1]) == 1 else 0.0)
#     urg = 0 if task['status'] == 'COMPLETED' else urg
#     urg = 0 if task['priority'] == -1 else urg
#     return urg


def gen_id(task):
    global PENDING_ID
    task['urg'] = calc_urg(task)
    return (task['title'], task['uuid'], task['urg'])


def load_pending():
    global PENDING, PENDING_ID
    if os.path.isfile(os.path.expanduser('~/.config/laboris/' + PENDING_FILE)):
        data = json.load(
            open(os.path.expanduser('~/.config/laboris/' + PENDING_FILE)))
        PENDING = {x['uuid']: x for x in data}
        PENDING_ID = sorted(
            [gen_id(x) for _, x in PENDING.items()],
            key=lambda x: get_uuid(x[1])['entryDate'])
        index = 0
        for task_id in PENDING_ID:
            if PENDING[task_id[1]]['dueDate']:
                PENDING[task_id[1]]['id'] = index + 1
                index += 1
        for task_id in PENDING_ID:
            if not PENDING[task_id[1]]['dueDate']:
                PENDING[task_id[1]]['id'] = index + 1
                index += 1


def save_pending():
    if not os.path.exists(os.path.expanduser('~/.config/laboris')):
        os.makedirs(os.path.expanduser('~/.config/laboris'))
    data = [{
        'title': x['title'],
        'projects': x['projects'],
        'tags': x['tags'],
        'entryDate': x['entryDate'],
        'dueDate': x['dueDate'],
        'doneDate': x['doneDate'],
        'priority': x['priority'],
        'modifiedDate': x['modifiedDate'],
        'status': x['status'],
        'times': x['times'],
        'uuid': x['uuid']
    } for _, x in PENDING.items()]
    json.dump(data,
              open(
                  os.path.expanduser('~/.config/laboris/' + PENDING_FILE), 'w'))


def load_completed():
    global COMPLETED, COMPLETED_ID
    if os.path.isfile(os.path.expanduser('~/.config/laboris/completed.json')):
        data = json.load(
            open(os.path.expanduser('~/.config/laboris/completed.json')))
        COMPLETED = {x['uuid']: x for x in data}
        COMPLETED_ID = [gen_id(x) for _, x in COMPLETED.items()]


def save_completed():
    if not os.path.exists(os.path.expanduser('~/.config/laboris')):
        os.makedirs(os.path.expanduser('~/.config/laboris'))
    data = [{
        'title': x['title'],
        'projects': x['projects'],
        'tags': x['tags'],
        'entryDate': x['entryDate'],
        'dueDate': x['dueDate'],
        'doneDate': x['doneDate'],
        'priority': x['priority'],
        'modifiedDate': x['modifiedDate'],
        'status': x['status'],
        'times': x['times'],
        'uuid': x['uuid']
    } for _, x in COMPLETED.items()]
    json.dump(data,
              open(os.path.expanduser('~/.config/laboris/completed.json'), 'w'))


def get_uuid(uuid):
    if uuid in PENDING:
        return PENDING[uuid]
    elif uuid in COMPLETED:
        return COMPLETED[uuid]


def fmt_task(tsk):
    task_color = CONFIG.get_color('urgency', tsk['urg'])
    if tsk['dueDate'] and datetime.datetime.fromtimestamp(tsk['dueDate']).date() == datetime.datetime.now().date():
        task_color = CONFIG.get_color('status.due-today')
    elif tsk['dueDate'] and datetime.datetime.fromtimestamp(tsk['dueDate']).date() < datetime.datetime.now().date():
        task_color = CONFIG.get_color('status.overdue')
    return Attr(tsk['title'], task_color) + (Attr(
        " +" + " +".join(tsk['projects']),
        CONFIG.get_color('comp.project')) if tsk['projects'] else '') + (
            Attr(" @" + " @".join(tsk['tags']), CONFIG.get_color('comp.tag'))
            if tsk['tags'] else '')


def task_long_name(task):
    return "{}{}{}".format(task['title'], (' +' + ' +'.join(task['projects'])
                                           if task['projects'] else ''),
                           (' @' + ' @'.join(task['tags'])
                            if task['tags'] else ''))


def start_active(tsk):
    if not tsk['times'] or len(tsk['times'][-1]) != 1:
        return Attr("Task is not active", CONFIG.get_color('msg.note'))
    diff = int(datetime.datetime.now().timestamp()) - tsk['times'][-1][0]
    minutes = diff // 60
    hour = minutes // 60
    minutes -= hour * 60
    return Attr("Task {} \"{}\" [{}]".format(tsk['id'], task_long_name(tsk),
                                             "{:02}:{:02}".format(
                                                 hour, minutes)),
                CONFIG.get_color('action.start'))


def stop_active(tsk):
    if tsk['times'] and len(tsk['times'][-1]) == 1:
        return Attr("Task is active", CONFIG.get_color('msg.note'))
    diff = tsk['times'][-1][1] - tsk['times'][-1][0]
    minutes = diff // 60
    hour = minutes // 60
    minutes -= hour * 60
    return Attr("Task {} \"{}\" [{}]".format(tsk['id'], task_long_name(tsk),
                                             "{:02}:{:02}".format(
                                                 hour, minutes)),
                CONFIG.get_color('action.stop'))


def fmt_task_uuid(uuid):
    return fmt_task(get_uuid(uuid))


def active_tasks():
    for _, task in PENDING.items():
        if task['times'] and len(task['times'][-1]) == 1:
            print(start_active(task))


def due_tasks():
    for _, task in PENDING.items():
        if task['dueDate'] and datetime.datetime.fromtimestamp(
                task['dueDate']).date() == datetime.datetime.now().date():
            print(fmt_task(task))


def overdue_tasks():
    for _, task in PENDING.items():
        if task['dueDate'] and datetime.datetime.fromtimestamp(
                task['dueDate']).date() < datetime.datetime.now().date():
            print(fmt_task(task))


def notes():
    overdue_tasks()
    due_tasks()
    active_tasks()


def get_task(string):
    task_id = []
    if string.isdigit() and int(string) - 1 < len(PENDING_ID):
        match_id = int(string)
        for task in PENDING_ID:
            if get_uuid(task[1])['id'] == match_id:
                return task
    for i in PENDING_ID:
        if i[0].lower().startswith(string.lower()) or i[1].startswith(string):
            task_id.append(i)
    if not task_id:
        for i in COMPLETED_ID:
            if i[0].lower().startswith(
                    string.lower()) or i[1].startswith(string):
                task_id.append(i)
    if not task_id:
        return None
    task_id = sorted(task_id, key=lambda x: x[2], reverse=True)
    if len(task_id) > 1:
        select = prompt.select("Specify Task: ",
                               [fmt_task_uuid(x[1]) for x in task_id])
        return task_id[select]
    return task_id[0]
