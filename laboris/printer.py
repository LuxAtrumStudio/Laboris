import settings as s
from color import fg, bg, stylize, attr


def print_task_set(task_set, fmt="id|p|age;abbr|project|due;abbr|description|urg"):
    fmt_split = fmt.split('|')
    sizes = [0] * len(fmt_split)
    for i, entry in enumerate(fmt_split):
        sizes[i] = len(entry.split(';')[0])
    for task in task_set:
        for i, entry in enumerate(fmt_split):
            sizes[i] = max(sizes[i], len(task.print_fmt(entry)))
    for i, entry in enumerate(fmt_split):
        entry = entry.split(';')[0]
        print(s._theme.get_color("title") + "{:{}}".format(entry.title(), sizes[i]) + s._theme.reset() + " ", end='')
    print()
    for i, task in enumerate(task_set):
        if i % 2 == 0:
            print(task.task_color(task.print_fmt(fmt, sizes)))
        else:
            print(s._theme.bg() + task.task_color(task.print_fmt(fmt, sizes)) + s._theme.reset())


def print_task_details(task, fmt="id|priority|description|status;long|project|tag|entry|due|done|urgency|uuid|times"):
    fmt = fmt.split('|')
    name_width = 0
    value_width = 0
    for entry in fmt:
        name_width = max(name_width, len(entry.split(';')[0]))
        value_width = max(value_width, len(task.print_fmt(entry)))
    print(s._theme.get_color("title") + "{:{}}".format("Name", name_width) + s._theme.reset() + " ", end='')
    print(s._theme.get_color("title") + "{:{}}".format("Value", value_width) + s._theme.reset())
    for i, entry in enumerate(fmt):
        if i % 2 == 0:
            print("{:<{}} {:<{}}".format(entry.split(';')[0].title(), name_width, task.print_fmt(entry), value_width))
        else:
            print(s._theme.bg() + "{:<{}} {:<{}}".format(entry.split(';')[0].title(), name_width, task.print_fmt(entry), value_width) + s._theme.reset())


def print_error(action, msg):
    if action == "add":
        print("{}Failed to add task\n{}{}".format(s._theme.get_color("err"), msg, s._theme.reset()))
    if action == "done":
        print("{}Failed to complete task\n{}{}".format(s._theme.get_color("err"), msg, s._theme.reset()))
    if action == "delete":
        print("{}Failed to complete task\n{}{}".format(s._theme.get_color("err"), msg, s._theme.reset()))
    if action == "start":
        print("{}Failed to start task\n{}{}".format(s._theme.get_color("err"), msg, s._theme.reset()))
    if action == "stop":
        print("{}Failed to stop task\n{}{}".format(s._theme.get_color("err"), msg, s._theme.reset()))


def print_action(action, task=None):
    if action == "add":
        print("{}Added task {}\n\'{}\'{}".format(s._theme.get_color("add"), task.id, task.description, s._theme.reset()))
    elif action == "done":
        print("{}Completed task {}\n\'{}\'{}".format(s._theme.get_color("completed"), task.id, task.description, s._theme.reset()))
    elif action == "delete":
        print("{}Deleted task {}\n\'{}\'{}".format(s._theme.get_color("delete"), task.id, task.description, s._theme.reset()))
    elif action == "start":
        print("{}Starting task {} \'{}\'{}".format(s._theme.get_color("start"), task.id, task.description, s._theme.reset()))
        print("{}Start    : {}{}".format(s._theme.get_color("start"), task.times[-1].print_start(True), s._theme.reset()))
        print("{}Stop     : {}{}".format(s._theme.get_color("start"), task.times[-1].print_end(True), s._theme.reset()))
        print("{}Duration : {}{}".format(s._theme.get_color("start"), task.times[-1].print_duration(True), s._theme.reset()))
    elif action == "stop":
        print("{}Stopping task {} \'{}\'{}".format(s._theme.get_color("stop"), task.id, task.description, s._theme.reset()))
        print("{}Start    : {}{}".format(s._theme.get_color("stop"), task.times[-1].print_start(True), s._theme.reset()))
        print("{}Stop     : {}{}".format(s._theme.get_color("stop"), task.times[-1].print_end(True), s._theme.reset()))
        print("{}Duration : {}{}".format(s._theme.get_color("stop"), task.times[-1].print_duration(True), s._theme.reset()))
