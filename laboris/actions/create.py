import datetime
import uuid

from laboris.smart_datetime import new
from laboris.color import Attr
from laboris.config import CONFIG
import laboris.task as ltask


def parse_args(args):
    data = {
        'title': None,
        'projects': None,
        'tags': None,
        'priority': None,
        'dueDate': 0
    }
    for arg in args:
        if arg.startswith('+'):
            if data['projects'] is None:
                data['projects'] = []
            if arg[1:] != 'None':
                data['projects'].append(arg[1:])
        elif arg.startswith('@'):
            if data['tags'] is None:
                data['tags'] = []
            if arg[1:] != 'None':
                data['tags'].append(arg[1:])
        elif arg.startswith('p:') and arg[2:].isdigit() or arg[2:] == '-1':
            data['priority'] = int(arg[2:])
        elif arg.startswith('due:'):
            data['dueDate'] = new(arg[4:])
        else:
            if data['title'] is None:
                data['title'] = ''
            data['title'] += arg + ' '
    if data['title']:
        data['title'] = data['title'][:-1]
    if data['dueDate'] and data['dueDate'] != 0:
        data['dueDate'] = int(data['dueDate'].timestamp())
    return data


def create_action(args):
    data = parse_args(args)
    task = {
        'title': data['title'] if data['title'] else '',
        'projects': data['projects'] if data['projects'] else [],
        'tags': data['tags'] if data['tags'] else [],
        'entryDate': int(datetime.datetime.now().timestamp()),
        'dueDate': data['dueDate'] if data['dueDate'] != 0 else None,
        'doneDate': None,
        'priority': data['priority'] if data['priority'] else 0,
        'modifiedDate': int(datetime.datetime.now().timestamp()),
        'status': 'PENDING',
        'times': []
    }
    task['uuid'] = str(
        uuid.uuid3(
            uuid.NAMESPACE_URL, task['title'] + datetime.datetime.fromtimestamp(
                task['entryDate']).strftime('%Y%m%d%H%M%S')))
    ltask.PENDING[task['uuid']] = task
    print(
        Attr('Created task \"{}\"'.format(ltask.task_long_name(task)),
             CONFIG.get_color('action.add')))


def modify_action(task, args):
    task = ltask.get_uuid(task[1])
    data = parse_args(args)
    for key in data:
        if data[key] is not None and key != 'dueDate':
            task[key] = data[key]
        elif key == 'dueDate' and data[key] != 0:
            task[key] = data[key]
    print(
        Attr('Modified \"{}\"'.format(ltask.task_long_name(task)),
             CONFIG.get_color('action.modify')))
