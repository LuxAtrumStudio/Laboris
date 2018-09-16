"""
, color.GetColor()List report
"""

import datetime

import laboris.task as task
import laboris.color as color
from laboris.config import CONFIG


def date_abbrev(lhs, rhs):
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


def print_task(fmt, tsk, title_pad, project_pad, tag_pad, use_color=True):
    data = {
        'id': tsk['id'] if 'id' in tsk else '',
        'uuid': tsk['uuid'],
        'uuidShort': tsk['uuid'][:8],
        'priority': tsk['priority'],
        'p': tsk['priority'] if tsk['priority'] != -1 else 0,
        'dueShort': date_abbrev(datetime.datetime.now(), tsk['dueDate']),
        'due': date_abbrev(datetime.datetime.now(), tsk['dueDate']),
        'title': "{:{}}".format(tsk['title'], title_pad),
        'age': date_abbrev(tsk['entryDate'], datetime.datetime.now()),
        'urg': tsk['urg'],
        'projects': "{:{}}".format(" ".join(tsk['projects']), project_pad),
        'tags': "{:{}}".format(" ".join(tsk['tags']), tag_pad)
    }
    if use_color:
        return color.Attr(
            fmt.format(data), CONFIG.get_color('urgency', tsk['urg']))
    else:
        return fmt.format(data)


def print_title(fmt, title_pad, project_pad, tag_pad):
    data = {
        'id': 'Id',
        'uuid': 'Uuid',
        'uuidShort': 'Uuid',
        'p': 'P',
        'age': 'Age',
        'due': 'Due',
        'dueShort': 'Due',
        'title': "{:{}}".format('Title', title_pad),
        'projects': "{:{}}".format('Projects', project_pad),
        'tags': "{:{}}".format("Tags", tag_pad),
        'urg': 'Urg'
    }
    fmt = fmt.replace('{', color.GetAttr(CONFIG.get_color('title')) + '{')
    fmt = fmt.replace('}', '}' + color.GetAttr('reset'))
    fmt = fmt.replace('f}', '}')
    return fmt.format(data)


def list_report(args):
    task.notes()
    longest_title = len('Title')
    longest_project = len('Projects')
    longest_tag = len('Tags')
    fmt = "{0[id]:2} {0[p]:1} {0[due]:>3} {0[title]} {0[projects]} {0[tags]} {0[urg]:6.3f}"
    tasks = task.PENDING_ID
    if args:
        if args[0].lower() == 'all':
            tasks = task.PENDING_ID + task.COMPLETED_ID
            fmt = "{0[uuidShort]:8} {0[p]:1} {0[due]:>4} {0[title]} {0[projects]} {0[tags]} {0[urg]:6.3f}"
        elif args[0].lower() == 'completed':
            tasks = task.COMPLETED_ID
            fmt = "{0[uuidShort]:8} {0[p]:1} {0[due]:>4} {0[title]} {0[projects]} {0[tags]} {0[urg]:6.3f}"
        elif args[0].lower() == 'pending':
            tasks = task.PENDING_ID
    for uuid in tasks:
        longest_title = max(longest_title, len(task.get_uuid(uuid[1])['title']))
        longest_tag = max(longest_tag,
                          len(" ".join(task.get_uuid(uuid[1])['tags'])))
        longest_project = max(longest_project,
                              len(" ".join(task.get_uuid(uuid[1])['projects'])))
    print(print_title(fmt, longest_title, longest_project, longest_tag))
    for i, uuid in enumerate(sorted(tasks, key=lambda x: x[2], reverse=True)):
        tsk = task.get_uuid(uuid[1])
        if task.get_uuid(uuid[1])['times'] and len(
                task.get_uuid(uuid[1])['times'][-1]) == 1:
            print(
                color.Attr(
                    print_task(fmt, task.get_uuid(uuid[1]),
                    longest_title,
                    longest_project,
                    longest_tag,
                    use_color=False), CONFIG.get_color('status.active')))
        elif tsk['status'] == 'PENDING' and tsk['dueDate'] and datetime.datetime.fromtimestamp(tsk['dueDate']).date() == datetime.datetime.now().date():
            print(
                color.Attr(
                    print_task(fmt, task.get_uuid(uuid[1]),
                    longest_title,
                    longest_project,
                    longest_tag,
                    use_color=False), CONFIG.get_color('status.due-today')))
        elif tsk['status'] == 'PENDING' and tsk['dueDate'] and datetime.datetime.fromtimestamp(tsk['dueDate']).date() < datetime.datetime.now().date():
            print(
                color.Attr(
                    print_task(fmt, task.get_uuid(uuid[1]),
                    longest_title,
                    longest_project,
                    longest_tag,
                    use_color=False), CONFIG.get_color('status.overdue')))
        elif i % 2 == 1:
            print(
                color.Attr(
                    print_task(fmt, task.get_uuid(uuid[1]), longest_title,
                               longest_project, longest_tag),
                    CONFIG.get_color('background'),
                    bg=True))
        else:
            print(
                print_task(fmt, task.get_uuid(uuid[1]), longest_title,
                           longest_project, longest_tag))
        # print("{0[id]} {0[priority]} {0[due]}".format(task.get_uuid(uuid[1])))
        # print_task("{.id:2} {p:}"task.get_uuid(uuid[1]))
