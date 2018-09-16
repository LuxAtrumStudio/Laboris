import datetime

import laboris.smart_datetime
import laboris.task
from laboris.color import GetAttr, Attr
import laboris.prompt as prompt
from laboris.config import CONFIG


def start_action(task, args):
    task = laboris.task.get_uuid(task[1])
    time = datetime.datetime.now()
    if args:
        time = laboris.smart_datetime.new(args[0])
    if task['times'] and len(task['times'][-1]) == 1:
        print(
            Attr("Warning: \"{}\" is already active".format(task['title']),
                 CONFIG.get_color('msg.warning')))
        print(laboris.task.start_active(task))
    else:
        task['times'].append([int(time.timestamp())])
        print(Attr("Starting Task", CONFIG.get_color('action.start')))
        print(laboris.task.start_active(task))


def stop_action(task, args):
    task = laboris.task.get_uuid(task[1])
    time = datetime.datetime.now()
    if args:
        time = laboris.smart_datetime.new(args[0])
    if not task['times'] or len(task['times'][-1]) != 1:
        print(
            Attr("Warning: \"{}\" is not active".format(task['title']),
                 CONFIG.get_color('msg.warning')))
    else:
        task['times'][-1].append(int(time.timestamp()))
        print(Attr("Stoping Task", CONFIG.get_color('action.stop')))
        print(laboris.task.stop_active(task))


def done_action(task, args):
    task = laboris.task.get_uuid(task[1])
    if task['status'] == 'COMPLETED':
        print(
            Attr(
                'Note: \"{}\" is already done'.format(
                    laboris.task.task_long_name(task)),
                CONFIG.get_color('msg.note')))
    else:
        task['status'] = 'COMPLETED'
        laboris.task.PENDING.pop(task['uuid'])
        laboris.task.COMPLETED[task['uuid']] = task
        print(
            Attr('Completed \"{}\"'.format(laboris.task.task_long_name(task)),
                 CONFIG.get_color('action.complete')))


def undone_action(task, args):
    task = laboris.task.get_uuid(task[1])
    if task['status'] == 'PENDING':
        print(
            Attr(
                'Note: \"{}\" is already pending'.format(
                    laboris.task.task_long_name(task)),
                CONFIG.get_color('msg.note')))
    else:
        task['status'] = 'PENDING'
        laboris.task.COMPLETED.pop(task['uuid'])
        laboris.task.PENDING[task['uuid']] = task
        print(
            Attr('UnCompleted \"{}\"'.format(laboris.task.task_long_name(task)),
                 CONFIG.get_color('action.add')))


def delete_action(task, args):
    task = laboris.task.get_uuid(task[1])
    if prompt.yn_choice(
            Attr('Delete \"{}\"'.format(laboris.task.task_long_name(task)),
                 CONFIG.get_color('action.delete')),
            style=GetAttr('yellow'),
            suggestion_style=GetAttr('yellow', 'bold'),
            default_style=GetAttr('cyan', 'bold'),
            default=False):
        if task['status'] == 'PENDING':
            laboris.task.PENDING.pop(task['uuid'])
        else:
            laboris.task.COMPLETED.pop(task['uuid'])
        print(
            Attr('Deleted \"{}\"'.format(laboris.task.task_long_name(task)),
                 CONFIG.get_color('action.delete')))
