import datetime
import laboris.task as ltask
from laboris.color import Attr
from laboris.config import CONFIG


def active_report(args):
    none = True
    for _, task in ltask.PENDING.items():
        if task['dueDate'] and datetime.datetime.fromtimestamp(
                task['dueDate']).date() < datetime.datetime.now().date():
            none = False
            print(
                Attr('Task \"{}\" Overdue'.format(ltask.task_long_name(task)),
                     CONFIG.get_color('status.overdue')))
    for _, task in ltask.PENDING.items():
        if task['dueDate'] and datetime.datetime.fromtimestamp(
                task['dueDate']).date() == datetime.datetime.now().date():
            none = False
            print(
                Attr('Task \"{}\" Due Today'.format(ltask.task_long_name(task)),
                     CONFIG.get_color('status.due-today')))
    for _, task in ltask.PENDING.items():
        if task['times'] and len(task['times'][-1]) == 1:
            none = False
            print(ltask.start_active(task))
    if none:
        print(Attr('No active tasks', CONFIG.get_color('msg.note')))
