from datetime import datetime

import laboris.settings as sett
import laboris.printer as printer
import laboris.sorter as sorter
import laboris.report as report
from laboris.interval import Interval
from laboris.task import Task


def run_action(args):
    if args.command == 'add':
        run_add(args)
    elif args.command == 'done':
        run_done(args)
    elif args.command == 'undone':
        run_undone(args)
    elif args.command == 'start':
        run_start(args)
    elif args.command == 'stop':
        run_stop(args)
    elif args.command == 'delete':
        run_delete(args)
    elif args.command == 'modify':
        run_modify(args)
    elif args.command == 'list':
        run_list(args)
    elif args.command == 'report':
        report.report(args)


def run_add(args):
    entry = datetime.now()
    cpy = args.description
    for word in args.description:
        if word.startswith('+'):
            if args.project is None:
                args.project = [word[1:]]
            else:
                args.project.append(word[1:])
            cpy.remove(word)
        elif word.startswith('@'):
            if args.tag is None:
                args.tag = [word[1:]]
            else:
                args.tag.append(word[1:])
            cpy.remove(word)
    args.description = " ".join(cpy)
    if args.tag is None:
        args.tag = list()
    if args.project is None:
        args.project = list()
    tsk = Task(args.description, args.project,
               args.tag, args.priority, entry, args.due)
    sett.pending.append(tsk)
    printer.print_action("add", tsk)


def run_done(args):
    tasks = find_task(args.task, True)
    if len(tasks[0]) == 0 and len(tasks[1]) == 0:
        printer.print_error("done", "No task found")
    else:
        if len(tasks[0]) != 0:
            task = tasks[0][0]
            task.done_date = datetime.now()
            if len(task.times) > 0 and task.times[-1].is_done() is False:
                task.times[-1].stop()
            sett.done.append(task)
            sett.pending.remove(task)
            printer.print_action("done", task)
        else:
            task = tasks[1][0]
            task.done_date = None
            sett.pending.append(task)
            sett.done.remove(task)
            printer.print_action("undone", task)


def run_undone(args):
    tasks = find_task(args.task, True)
    if len(tasks[1]) == 0:
        printer.print_error("undone", "No task found")
    else:
        task = tasks[1][0]
        task.done_date = None
        sett.pending.append(task)
        sett.done.remove(task)
        printer.print_action("undone", task)


def run_start(args):
    tasks = find_task(args.task, True)
    tasks = tasks[0] + tasks[1]
    if len(tasks) == 0:
        printer.print_error("start", "No task found")
    else:
        task = tasks[0]
        if len(task.times) > 0 and task.times[-1].is_done() is False:
            printer.print_error("start", "Task is already started")
            return
        task.times.append(Interval(args.time))
        printer.print_action("start", task)
        tmp_set = sett.pending
        sorter.sort_task_set(tmp_set, "urg")
        if task.urgency < tmp_set[0].urgency:
            printer.print_action('urg')


def run_stop(args):
    tasks = find_task(args.task, True)
    tasks = tasks[0] + tasks[1]
    if len(tasks) == 0:
        printer.print_error("stop", "No task found")
    else:
        task = tasks[0]
        if task.times[-1].is_done() is False:
            task.times[-1].stop(args.time)
            printer.print_action('stop', task)
        else:
            printer.print_error(
                'stop', "Task {} has not been started".format(task.print_id()))


def run_delete(args):
    tasks = find_task(args.task, True)
    if len(tasks[0]) == 0 and len(tasks[1]) == 0:
        printer.print_error("delete", "No task found")
    elif len(tasks[0]) != 0:
        task = tasks[0][0]
        sett.pending.remove(task)
        printer.print_action("delete", task)
    elif len(tasks[1]) != 0:
        task = tasks[1][0]
        sett.done.remove(task)
        printer.print_action("delete", task)


def run_modify(args):
    tasks = find_task(args.task, True)
    tasks = tasks[0] + tasks[1]
    if len(tasks) == 0:
        printer.print_error('modify', "No task found")
    else:
        task = tasks[0]
        if args.description != list():
            task.description = ' '.join(args.description)
        if args.due is not None:
            task.due_date = args.due
        if args.priority is not None:
            task.priority = args.priority
        if args.project is not None:
            task.project = args.project
        if args.tag is not None:
            task.tag = args.tag
        printer.print_action('modify', task)


def run_list(args):
    tasks = find_task(args.task)
    if len(tasks[0]) == 0 and len(tasks[1]) == 0:
        tasks = sett.pending, sett.done
    if args.group == 'all':
        if args.format is None:
            args.format = "id|st|uuid;short|age;abbr|done;abbr|p|project|due;date|description"
        tasks = tasks[0] + tasks[1]
    elif args.group == 'completed':
        if args.format is None:
            args.format = "uuid;short|entry;date|done;date|age;abbr|p|project|due;date|description"
        tasks = tasks[1]
    elif args.group == 'due':
        if args.format is None:
            args.format = "id|p|age;abbr|project|due;abbr|description|urg"
        tmp = list()
        for tsk in tasks[0]:
            if tsk.is_due() is True:
                tmp.append(tsk)
        tasks = tmp
    else:
        if args.format is None:
            args.format = "id|p|age;abbr|project|due;abbr|description|urg"
        tasks = tasks[0]
    if len(tasks) == 1:
        printer.print_task_details(tasks[0])
    else:
        if args.sort is not None:
            sorter.sort_task_set(tasks, args.sort)
        else:
            sorter.sort_task_set(tasks, "urg")
        printer.print_active()
        printer.print_task_set(tasks, args.format)


def find_task(ref, strict=False):
    tasks = list()
    completed = list()
    if ref is None:
        return tasks, completed
    for task in sett.pending:
        if ref == str(task.id):
            tasks.append(task)
            return tasks, completed
    for task in sett.pending:
        if task.print_uuid("long").startswith(ref):
            tasks.append(task)
            return tasks, completed
    for task in sett.done:
        if task.print_uuid("long").startswith(ref):
            completed.append(task)
            return tasks, completed
    for task in sett.pending:
        if task.description.startswith(ref):
            tasks.append(task)
    for task in sett.done:
        if task.description.startswith(ref):
            completed.append(task)
    if len(tasks) != 0 or len(completed) != 0:
        return tasks, completed
    for task in sett.pending:
        if ref in task.project:
            tasks.append(task)
    for task in sett.done:
        if ref in task.project:
            completed.append(task)
    if len(tasks) != 0 or len(completed) != 0:
        return tasks, completed
    for task in sett.pending:
        if ref in task.tag:
            tasks.append(task)
    for task in sett.done:
        if ref in task.tag:
            completed.append(task)
    if len(tasks) > 0:
        tasks = [tasks[0]]
    if len(completed) > 0:
        completed = [completed[0]]
    return tasks, completed
