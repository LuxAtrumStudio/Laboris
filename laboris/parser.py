import re
from enum import Enum
from datetime import datetime, timedelta

import laboris.settings as s
import laboris.sorter as sorter
import laboris.task as task
import laboris.printer as printer
import laboris.interval as interval
import sys
import laboris.report as report

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
    MODIFY = 8
    UNDONE = 9


def parse_args():
    global args
    global data
    args = sys.argv[1:]
    rep = report.is_report(args)
    if rep is not None:
        find_project()
        find_tag()
        report.report(rep, args, data)
        return
    find_args()
    action = find_action()
    find_project()
    find_tag()
    action_print(action)
    if action is Action.ADD:
        action_add()
    elif action is Action.DONE:
        action_done()
    elif action is Action.UNDONE:
        action_undone()
    elif action is Action.START:
        action_start()
    elif action is Action.STOP:
        action_stop()
    elif action is Action.DELETE:
        action_delete()
    elif action is Action.MODIFY:
        action_modify()


def action_modify():
    global data
    global args
    print(data)
    find_task(True)
    if "_task" in data and type(data["_task"]) is task.Task:
        if "priority" in data:
            data["_task"].priority = int(data["priority"])
        elif "p" in data:
            data["_task"].priority = int(data["p"])
        if "due" in data:
            print("HERE")
            data["_task"].due_date = get_date(data["due"])
        if len(data["_project"]) != 0:
            data["_task"].project = data["_project"]
        if len(data["_tag"]) != 0:
            data["_task"].tag = data["_tag"]
        if len(args) != 0:
            data["_task"].description = " ".join(args)
        printer.print_action("modify", data["_task"])
    elif "_completed_task" in data and type(
            data["_completed_task"]) is task.Task:
        if "priority" in data:
            data["_comleted_task"].priority = int(data["priority"])
        elif "p" in data:
            data["_comleted_task"].priority = int(data["p"])
        if "due" in data:
            data["_comleted_task"].due = get_date(data["due"])
        if len(data["_project"]) != 0:
            data["_comleted_task"].project = data["_project"]
        if len(data["_tag"]) != 0:
            data["_comleted_task"].tag = data["_tag"]
        if len(args) != 0:
            data["_comleted_task"].description = " ".join(args)
        printer.print_action("modify", data["_completed_task"])
    else:
        printer.print_error("modify", "No task found")


def action_delete():
    find_task()
    if "_task" in data and type(data["_task"]) is task.Task:
        s._pending.remove(data["_task"])
        printer.print_action("delete", data["_task"])
    elif "_completed_task" in data and type(
            data["_completed_task"]) is task.Task:
        s._done.remove(data["_completed_task"])
        printer.print_action("delete", data["_completed_task"])
    else:
        printer.print_error("delete", "No task found")


def action_stop():
    find_task()
    if "_task" in data and type(data["_task"]) is task.Task:
        if len(data["_task"]
               .times) != 0 and data["_task"].times[-1].is_done() is False:
            data["_task"].times[-1].stop()
            printer.print_action("stop", data["_task"])
        else:
            printer.print_error(
                "stop",
                "Task {} has not been started".format(data["_task"].print_id()))
    else:
        printer.print_error("stop", "No task found")


def action_start():
    find_task()
    if "_task" in data and type(data["_task"]) is task.Task:
        data["_task"].times.append(interval.Interval())
        printer.print_action("start", data["_task"])
        tmp_set = s._pending
        sorter.sort_task_set(tmp_set, "urg")
        if data["_task"].urgency < tmp_set[0].urgency:
            printer.print_action("urg")
    else:
        printer.print_error("start", "No task found")


def action_done():
    find_task()
    if "_task" not in data and "_completed_task" not in data:
        return
    if "_task" in data:
        if type(data["_task"]) is task.Task:
            if data["_task"].active is True:
                data["_task"].times[-1].stop()
                printer.print_action("stop", data["_task"])
            data["_task"].done_date = datetime.now()
            s._done.append(data["_task"])
            s._pending.remove(data["_task"])
            printer.print_action("done", data["_task"])
        else:
            printer.print_error("done", "Cannot specify multiple tasks")
    elif "_completed_task" in data:
        if type(data["_completed_task"]) is task.Task:
            s._done.remove(data["_completed_task"])
            s._pending.append(data["_completed_task"])
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
        due = get_date(data["due"])
    new_task = task.Task(" ".join(args), data["_project"], data["_tag"], pri,
                         entry, due)
    s._pending.append(new_task)
    printer.print_action("add", new_task)


def action_print(action):
    global data
    global args
    if action not in [Action.NONE, Action.LIST, Action.SHOW]:
        return
    find_task()
    if (action is Action.NONE or action is Action.SHOW
       ) and "_task" in data and type(data["_task"]) is task.Task:
        printer.print_task_details(data["_task"])
    elif (action is Action.NONE or
          action is Action.SHOW) and "_completed_task" in data and type(
              data["_completed_task"]) is task.Task:
        printer.print_task_details(data["_completed_task"])
    elif action is Action.NONE or action is Action.LIST:
        fmt = "id|p|age;abbr|project|due;abbr|description|urg"
        task_set = None
        if "_task" in data and type(data["_task"]) is list:
            task_set = data["_task"]
        if "all" in args:
            fmt = "id|st|uuid;short|age;abbr|done;abbr|p|project|due;date|description"
            if task_set is None:
                task_set = s._pending + s._done
            elif "_completed_task" in data:
                task_set += data["_completed_task"]
        elif "completed" in args:
            fmt = "uuid;short|entry;date|done;date|age;abbr|p|project|due;date|description"
            if task_set is None:
                task_set = s._done
            elif "_completed_task" in data:
                task_set = data["_completed_task"]
        elif "_task" not in data:
            task_set = s._pending
        task_set = get_project_set(task_set)
        task_set = get_tag_set(task_set)
        if "sort" in data:
            sorter.sort_task_set(task_set, data["sort"])
        else:
            sorter.sort_task_set(task_set, "urg")
        printer.print_active()
        printer.print_task_set(task_set, fmt)


def attempt_date(string, fmt):
    try:
        dt = datetime.strptime(string, fmt)
        if fmt == "%A":
            cdt = datetime.now()
            string = string.title()
            while cdt.strftime("%A") != string:
                cdt += timedelta(days=1)
            dt = dt.replace(
                year=cdt.year,
                month=cdt.month,
                day=cdt.day,
                hour=0,
                minute=0,
                second=0)
        if fmt.startswith("%AT"):
            string = string.split('T')[0]
            cdt = datetime.now()
            string = string.title()
            while cdt.strftime("%A") != string:
                cdt += timedelta(days=1)
            dt = dt.replace(year=cdt.year, month=cdt.month, day=cdt.day)
    except ValueError:
        return False
    return dt


def try_date_format_set(arg, fmts):
    for fmt in fmts:
        if attempt_date(arg, fmt) is not False:
            return attempt_date(arg, fmt)
    return None


def get_date(arg):
    arg = arg.replace("@", "T")
    dmy = [
        "%d-%m-%Y", "%d-%m-%y", "%m-%d-%Y", "%m-%d-%y", "%Y-%m-%d", "%y-%m-%d",
        "%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d", "%y/%m/%d"
    ]
    dmyhm = [
        "%d-%m-%YT%H:%M", "%d-%m-%yT%H:%M", "%m-%d-%YT%H:%M", "%m-%d-%yT%H:%M",
        "%Y-%m-%dT%H:%M", "%y-%m-%dT%H:%M", "%d/%m/%YT%H:%M", "%d/%m/%yT%H:%M",
        "%m/%d/%YT%H:%M", "%m/%d/%yT%H:%M", "%Y/%m/%dT%H:%M", "%y/%m/%dT%H:%M"
    ]
    a = ["%A"]
    ahm = ["%AT%H:%M", "%AT%H:%M:%S"]
    dm = ["%d-%m", "%m-%d", "%d/%m", "%m/%d"]
    hms = ["%H:%M", "%H.%M", "%H:%M:%S", "%H.%M.%S"]

    arg = arg.replace(
        "yesterday", (datetime.now() - timedelta(days=1)).strftime("%A"))
    arg = arg.replace("today", datetime.now().strftime("%A"))
    arg = arg.replace(
        "tomorrow", (datetime.now() + timedelta(days=1)).strftime("%A"))
    arg = arg.replace(
        "Yesterday", (datetime.now() - timedelta(days=1)).strftime("%A"))
    arg = arg.replace("Today", datetime.now().strftime("%A"))
    arg = arg.replace(
        "Tomorrow", (datetime.now() + timedelta(days=1)).strftime("%A"))
    dt = datetime.now()
    adt = try_date_format_set(arg, dmy)
    if adt is not None:
        return dt.replace(year=adt.year, month=adt.month, day=adt.day)
    adt = try_date_format_set(arg, dm)
    if adt is not None:
        return dt.replace(month=adt.month, day=adt.day)
    adt = try_date_format_set(arg, hms)
    if adt is not None:
        return dt.replace(hour=adt.hour, minute=adt.minute, second=adt.second)
    adt = try_date_format_set(arg, dmyhm)
    if adt is not None:
        return adt
    adt = try_date_format_set(arg, a)
    if adt is not None:
        return adt
    adt = try_date_format_set(arg, ahm)
    if adt is not None:
        return adt
    printer.print_error("date", "Invalid date format: \"{}\"".format(arg))
    return datetime.now()


def get_project_set(task_set):
    rem = list()
    for task in task_set:
        if set(data["_project"]) <= set(task.project):
            rem.append(task)
    return rem


def get_tag_set(task_set):
    rem = list()
    for task in task_set:
        if set(data["_tag"]) <= set(task.tag):
            rem.append(task)
    return rem


def find_task(strict=False):
    global args
    global data
    task_ref = list()
    for entry in args:
        for task in s._pending:
            if entry == str(task.id) and entry != str():
                data["_task"] = task
                args.remove(entry)
                return
    for entry in args:
        for task in s._pending:
            if task.print_uuid("long").startswith(entry) and entry != str():
                data["_task"] = task
                args.remove(entry)
                return
        for task in s._done:
            if task.print_uuid("long").startswith(entry) and entry != str():
                data["_completed_task"] = task
                args.remove(entry)
                return
    if strict is True:
        return
    for entry in args:
        for task in s._pending:
            if task.description.startswith(entry) and entry != str():
                if "_task" not in data:
                    data["_task"] = list()
                data["_task"].append(task)
                task_ref.append(entry)
        for task in s._done:
            if task.description.startswith(entry) and entry != str():
                if "_completed_task" not in data:
                    data["_completed_task"] = list()
                data["_completed_task"].append(task)
                task_ref.append(entry)
    if "_tasks" not in data and "_completed_task" not in data:
        for entry in args:
            for task in s._pending:
                if entry in task.project:
                    if "_task" not in data:
                        data["_task"] = list()
                    data["_task"].append(task)
                    task_ref.append(entry)
            for task in s._done:
                if entry in task.project:
                    if "_completed_task" not in data:
                        data["_completed_task"] = list()
                    data["_completed_task"].append(task)
                    task_ref.append(entry)
    if "_tasks" not in data and "_completed_task" not in data:
        for entry in args:
            for task in s._pending:
                if entry in task.tag:
                    if "_task" not in data:
                        data["_task"] = list()
                    data["_task"].append(task)
                    task_ref.append(entry)
            for task in s._done:
                if entry in task.tag:
                    if "_completed_task" not in data:
                        data["_completed_task"] = list()
                    data["_completed_task"].append(task)
                    task_ref.append(entry)
    args = [x for x in args if x not in task_ref]
    if "_task" in data and len(
            data["_task"]) == 1 and "_completed_task" not in data:
        data["_task"] = data["_task"][0]
    if "_completed_task" in data and len(
            data["_completed_task"]) == 1 and "_task" not in data:
        data["_completed_task"] = data["_completed_task"][0]
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
    actions = {
        "add": Action.ADD,
        "show": Action.SHOW,
        "done": Action.DONE,
        "delete": Action.DELETE,
        "start": Action.START,
        "stop": Action.STOP,
        "modify": Action.MODIFY,
        "undone": Action.UNDONE
    }
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
        entry = ":".join(entry.split(':')[1:])
        data[name] = entry


def remove(l, v):
    l[:] = [x for x in l if not v]
