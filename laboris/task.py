"""
Task query system
"""

import os
import json
import datetime

from laboris.color import Attr
from laboris.config import CONFIG
import laboris.prompt as prompt

PENDING = {}
PENDING_ID = []
COMPLETED = {}
COMPLETED_ID = []

PENDING_FILE = "new.json"


def urgency_age(task):
    diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(
        task['entryDate'])
    age = diff.days + (diff.seconds / 86400)
    return age / 400


def urgency_due(task):
    if task['dueDate'] is None:
        return 0.0
    late = False
    if datetime.datetime.now() > datetime.datetime.fromtimestamp(
            task['dueDate']):
        diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(
            task['dueDate'])
        late = True
    else:
        diff = datetime.datetime.fromtimestamp(
            task['dueDate']) - datetime.datetime.now()
    overdue = diff.days + (diff.seconds / 86400)
    if late is False:
        overdue *= -1
    if overdue > 7:
        return 1.0
    elif overdue >= -14:
        return float((overdue + 14.0) * 0.8 / 21.0) + 0.2
    return 0.2


def calc_urg(task):
    urg = 0.0
    urg += abs(2.00 * urgency_age(task))
    urg += abs(12.0 * urgency_due(task))
    urg += abs(1.00 * task['priority'])
    urg += abs(0.20 * len(task['tags']))
    urg += abs(1.00 * len(task['projects']))
    urg += abs(4.0 if task['times'] and len(task['times'][-1]) == 1 else 0.0)
    urg = 0 if task['status'] == 'COMPLETED' else urg
    urg = 0 if task['priority'] == -1 else urg
    return urg


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
        PENDING_ID = sorted([gen_id(x) for _, x in PENDING.items()],
                            key=lambda x: get_uuid(x[1])['entryDate'])
        for i, index in enumerate(PENDING_ID):
            PENDING[index[1]]['id'] = i + 1


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
    json.dump(
        data, open(
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
    return Attr(tsk['title'], CONFIG.get_color('urgency', tsk['urg'])) + (Attr(
        " +" + " +".join(tsk['projects']),
        CONFIG.get_color('comp.project')) if tsk['projects'] else '') + (Attr(
            " @" + " @".join(tsk['tags']),
            CONFIG.get_color('comp.tag')) if tsk['tags'] else '')


def task_long_name(task):
    return "{}{}{}".format(
        task['title'],
        (' +' + ' +'.join(task['projects']) if task['projects'] else ''),
        (' @' + ' @'.join(task['tags']) if task['tags'] else ''))


def start_active(tsk):
    if not tsk['times'] or len(tsk['times'][-1]) != 1:
        return Attr("Task is not active", CONFIG.get_color('msg.note'))
    diff = int(datetime.datetime.now().timestamp()) - tsk['times'][-1][0]
    minutes = diff // 60
    hour = minutes // 60
    minutes -= hour * 60
    return Attr(
        "Task {} \"{}\" [{}]".format(tsk['id'], task_long_name(tsk),
                                     "{:02}:{:02}".format(hour, minutes)),
        CONFIG.get_color('action.start'))


def stop_active(tsk):
    if tsk['times'] and len(tsk['times'][-1]) == 1:
        return Attr("Task is active", CONFIG.get_color('msg.note'))
    diff = tsk['times'][-1][1] - tsk['times'][-1][0]
    minutes = diff // 60
    hour = minutes // 60
    minutes -= hour * 60
    return Attr(
        "Task {} \"{}\" [{}]".format(tsk['id'], task_long_name(tsk),
                                     "{:02}:{:02}".format(hour, minutes)),
        CONFIG.get_color('action.stop'))


def fmt_task_uuid(uuid):
    return fmt_task(get_uuid(uuid))


def get_task(string):
    task_id = []
    if string.isdigit() and int(string) - 1 < len(PENDING_ID):
        return PENDING_ID[int(string) - 1]
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
