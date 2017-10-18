import re
from enum import Enum
from datetime import datetime

import settings as s
import sorter
import task
import printer
import interval
import sys


args = list()
data = dict()


class Action(Enum):
    NONE = 0
    ADD = 1
    SHOW = 2
    DONE = 3
    LIST = 4
    START = 5
    STOP = 6
    DELETE = 7


def parse_args():
    global args
    global data
    args = sys.argv[1:]
    find_args()
    action = find_action()
    find_project()
    find_tag()
    action_print(action)
    if action is Action.ADD:
        action_add()
    elif action is Action.DONE:
        action_done()
    elif action is Action.START:
        action_start()
    elif action is Action.STOP:
        action_stop()


def action_stop():
    find_task()
    if "_task" in data and type(data["_task"]) is task.Task:
        if len(data["_task"].times) != 0 and data["_task"].times[-1].is_done() is False:
            data["_task"].times[-1].stop()
            printer.print_action("stop", data["_task"])
        else:
            printer.print_error("stop", "Task {} has not been started".format(data["_task"].print_id()))
    else:
        printer.print_error("stop", "No task found")


def action_start():
    find_task()
    if "_task" in data and type(data["_task"]) is task.Task:
        data["_task"].times.append(interval.Interval())
        printer.print_action("start", data["_task"])
    else:
        printer.print_error("start", "No task found")


def action_done():
    find_task()
    if "_task" not in data and "_completed_task" not in data:
        return
    if "_task" in data:
        if type(data["_task"]) is task.Task:
            s._done.append(data["_task"])
            s._pending.remove(data["_task"])
            printer.print_action("done", data["_task"])
        else:
            printer.print_error("done", "Cannot specify multiple tasks")
    elif "_completed_task" in data:
        if type(data["_completed_task"]) is task.Task:
            s._done.remove(data["_completed_task"])
            s._pending.pending(data["_completed_task"])
            printer.print_action("done", data["_completed_task"])
        else:
            printer.print_error("done", "Cannot specify multiple tasks")


def action_add():
    global args
    global data
    pri = 0
    entry = datetime.now()
    due = None
    if len(args) == 0:
        printer.print_error("add", "Task must have description")
        return
    if "priority" in data:
        pri = int(data["priority"])
    elif "p" in data:
        pri = int(data["p"])
    elif "due" in data:
        due = get_datetime(data["due"])
    new_task = task.Task(" ".join(args), data["_project"], data["_tag"], pri, entry, due)
    s._pending.append(new_task)
    printer.print_action("add", new_task)


def action_print(action):
    global data
    global args
    if action not in [Action.NONE, Action.LIST, Action.SHOW]:
        return
    find_task()
    if (action is Action.NONE or action is Action.SHOW) and "_task" in data and type(data["_task"]) is task.Task:
        printer.print_task_details(data["_task"])
    elif action is Action.NONE or action is Action.LIST:
        task_set = None
        if "_task" in data and type(data["_task"]) is list:
            task_set = data["_task"]
        if "all" in args:
            if task_set is None:
                task_set = s._pending + s._done
            elif "_completed_task" in data:
                task_set += data["_completed_task"]
        elif "completed" in args:
            if task_set is None:
                task_set = s._done
            elif "_completed_task" in data:
                task_set = data["_completed_task"]
        elif "_task" not in data:
            task_set = s._pending
        get_project_set(task_set)
        get_tag_set(task_set)
        if "sort" in data:
            sorter.sort_task_set(task_set, data["sort"])
        else:
            sorter.sort_task_set(task_set, "urg")
        printer.print_task_set(task_set)


def get_datetime(val):
    return datetime.now()


def get_project_set(task_set):
    rem = list()
    for task in task_set:
        if set(data["_project"]) <= set(task.project):
            rem.append(task)
    task_set[:] = rem


def get_tag_set(task_set):
    rem = list()
    for task in task_set:
        if set(data["_tag"]) <= set(task.tag):
            rem.append(task)
    task_set[:] = rem


def find_task():
    global args
    global data
    task_ref = list()
    for entry in args:
        was_added = False
        for task in s._pending:
            if entry == str(task.id) or entry == task.print_uuid("short") or entry == task.print_uuid("long"):
                data["_task"] = task
                args.remove(entry)
                return
            elif task.description.startswith(entry):
                if "_task" not in data:
                    data["_task"] = list()
                data["_task"].append(task)
                task_ref.append(entry)
        for task in s._done:
            if entry == task.print_uuid("short") or entry == task.print_uuid("long"):
                data["_task"] = task
                args.remove(entry)
                return
            elif task.description.startswith(entry):
                if "_completed_task" not in data:
                    data["_completed_task"] = list()
                data["_completed_task"].append(task)
                task_ref.append(entry)
    args = [x for x in args if x not in task_ref]
    return


def find_project():
    global args
    global data
    data["_project"] = [x[1:] for x in args if x.startswith("+")]
    args = [x for x in args if x[1:] not in data["_project"]]


def find_tag():
    global args
    global data
    data["_tag"] = [x[1:] for x in args if x.startswith("@")]
    args = [x for x in args if x[1:] not in data["_tag"]]


def find_action():
    global args
    actions = {"add": Action.ADD, "show": Action.SHOW, "done": Action.DONE, "delete": Action.DELETE,
               "start": Action.START, "stop": Action.STOP}
    for entry in args:
        if entry.lower() in actions.keys():
            args.remove(entry)
            return actions[entry.lower()]
    return Action.NONE


def find_args():
    global args
    global data
    r = re.compile(".*:.*")
    res = [x for x in args if r.match(x)]
    args = [x for x in args if x not in res]
    for entry in res:
        name = entry.split(':')[0]
        entry = " ".join(entry.split(':')[1:])
        data[name] = entry


def remove(l, v):
    l[:] = [x for x in l if not v]
