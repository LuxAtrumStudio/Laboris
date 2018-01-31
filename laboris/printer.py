import laboris.settings as s


def print_active():
    has_print = False
    for task in s.pending:
        if task.active is True:
            print("{}Task {} \'{}\' [{}]{}".format(
                s.theme.get_color("start"), task.id, task.description,
                task.times[-1].print_duration(True), s.theme.reset()))
            has_print = True
    if has_print is True:
        print()


def print_task_set(task_set,
                   fmt="id|p|age;abbr|project|due;abbr|description|urg"):
    fmt = fmt.replace(',', '|')
    fmt = fmt.replace(':', ';')
    if len(task_set) == 0:
        print(s.theme.get_color("title") + "No Tasks" + s.theme.reset())
        return
    fmt_split = fmt.split('|')
    sizes = [0] * len(fmt_split)
    for i, entry in enumerate(fmt_split):
        sizes[i] = len(entry.split(';')[0])
    for task in task_set:
        for i, entry in enumerate(fmt_split):
            sizes[i] = max(sizes[i], len(task.print_fmt(entry)))
    for i, entry in enumerate(fmt_split):
        entry = entry.split(';')[0]
        print(
            s.theme.get_color("title") + "{:{}}".format(
                entry.title(), sizes[i]) + s.theme.reset() + " ",
            end='')
    print()
    for i, task in enumerate(task_set):
        if i % 2 == 0:
            print(task.task_color(task.print_fmt(fmt, sizes)))
        else:
            print(s.theme.bg() + task.task_color(task.print_fmt(fmt, sizes)) +
                  s.theme.reset())


def print_task_details(
        task,
        fmt="id|priority|description|status;long|project|tag|entry|due|done|urgency|uuid|times"
):

    fmt = fmt.split('|')
    name_width = 0
    value_width = 0
    for entry in fmt:
        name_width = max(name_width, len(entry.split(';')[0]))
        if entry not in ["project", "tag", "times"]:
            value_width = max(value_width, len(task.print_fmt(entry)))
        else:
            value_width = max(value_width, len(task.print_fmt(entry + ";size")))
    print(
        s.theme.get_color("title") + "{:{}}".format("Name", name_width) +
        s.theme.reset() + " ",
        end='')
    print(
        s.theme.get_color("title") + "{:{}}".format("Value", value_width) +
        s.theme.reset())
    i = 0
    for entry in fmt:
        if i % 2 == 0:
            if entry not in ["project", "tag", "times"]:
                print("{:<{}} {:<{}}".format(
                    entry.split(';')[0].title(), name_width,
                    task.print_fmt(entry), value_width))
                i += 1
            else:
                se = list()
                if entry == "project":
                    se = task.project
                elif entry == "tag":
                    se = task.tag
                elif entry == "times":
                    se = task.times
                for j in range(0, len(se)):
                    if j == 0:
                        print("{:<{}} {:<{}}".format(
                            entry.split(';')[0].title(), name_width,
                            task.print_fmt(entry + ";" + str(j)), value_width))
                    elif j == len(se) - 1:
                        print("{:<{}} \033[4m{:<{}}\033[0m".format(
                            entry.split(';')[0].title(), name_width,
                            task.print_fmt(entry + ";" + str(j)), value_width))
                    else:
                        print("{:<{}} {:<{}}".format(
                            "", name_width,
                            task.print_fmt(entry + ";" + str(j)), value_width))
                    i += 1
                if entry == "times":
                    print("{:<{}} {:<{}}".format("Total", name_width,
                                                 task.print_fmt("times;total"),
                                                 value_width))
        else:
            if entry not in ["project", "tag", "times"]:
                print(s.theme.bg() + "{:<{}} {:<{}}".format(
                    entry.split(';')[0].title(), name_width,
                    task.print_fmt(entry), value_width) + s.theme.reset())
                i += 1
            else:
                se = list()
                if entry == "project":
                    se = task.project
                elif entry == "tag":
                    se = task.tag
                elif entry == "times":
                    se = task.times
                for j in range(0, len(se)):
                    if j == 0:
                        print(s.theme.bg() + "{:<{}} {:<{}}".format(
                            entry.split(';')[0].title(), name_width,
                            task.print_fmt(entry + ";" + str(j)), value_width) +
                              s.theme.reset())
                    elif j == len(se) - 1:
                        print(s.theme.bg() + "{:<{}} \033[4m{:<{}}".format(
                            entry.split(';')[0].title(), name_width,
                            task.print_fmt(entry + ";" + str(j)), value_width) +
                              s.theme.reset())
                    else:
                        print(s.theme.bg() + "{:<{}} {:<{}}".format(
                            "", name_width,
                            task.print_fmt(entry + ";" + str(j)), value_width) +
                              s.theme.reset())
                    i += 1
                if entry == "times":
                    print(s.theme.bg() + "{:<{}} {:<{}}".format(
                        "Total", name_width,
                        task.print_fmt("times;total"), value_width) +
                          s.theme.reset())


def print_error(action, msg):
    if action == "add":
        print("{}Failed to add task\n{}{}".format(
            s.theme.get_color("err"), msg, s.theme.reset()))
    elif action == "done":
        print("{}Failed to complete task\n{}{}".format(
            s.theme.get_color("err"), msg, s.theme.reset()))
    elif action == "delete":
        print("{}Failed to complete task\n{}{}".format(
            s.theme.get_color("err"), msg, s.theme.reset()))
    elif action == "start":
        print("{}Failed to start task\n{}{}".format(
            s.theme.get_color("err"), msg, s.theme.reset()))
    elif action == "stop":
        print("{}Failed to stop task\n{}{}".format(
            s.theme.get_color("err"), msg, s.theme.reset()))
    elif action == "modify":
        print("{}Failed to modify task\n{}{}".format(
            s.theme.get_color("err"), msg, s.theme.reset()))
    else:
        print("{}{}{}".format(s.theme.get_color("err"), msg, s.theme.reset()))


def print_action(action, task=None):
    if action == "add":
        print("{}Added task {}\n\'{}\'{}".format(
            s.theme.get_color("add"), task.id, task.description,
            s.theme.reset()))
    elif action == "done":
        print("{}Completed task {}\n\'{}\'{}".format(
            s.theme.get_color("completed"), task.id, task.description,
            s.theme.reset()))
    elif action == "delete":
        print("{}Deleted task {}\n\'{}\'{}".format(
            s.theme.get_color("delete"), task.id, task.description,
            s.theme.reset()))
    elif action == "start":
        print("{}Starting task {} \'{}\'{}".format(
            s.theme.get_color("start"), task.id, task.description,
            s.theme.reset()))
        print("{}Start    : {}{}".format(
            s.theme.get_color("start"), task.times[-1].print_start(True),
            s.theme.reset()))
        print("{}Current  : {}{}".format(
            s.theme.get_color("start"), task.times[-1].print_end(True),
            s.theme.reset()))
        print("{}Duration : {}{}".format(
            s.theme.get_color("start"), task.times[-1].print_duration(True),
            s.theme.reset()))
    elif action == "stop":
        print("{}Stopping task {} \'{}\'{}".format(
            s.theme.get_color("stop"), task.id, task.description,
            s.theme.reset()))
        print("{}Start    : {}{}".format(
            s.theme.get_color("stop"), task.times[-1].print_start(True),
            s.theme.reset()))
        print("{}Stop     : {}{}".format(
            s.theme.get_color("stop"), task.times[-1].print_end(True),
            s.theme.reset()))
        print("{}Duration : {}{}".format(
            s.theme.get_color("stop"), task.times[-1].print_duration(True),
            s.theme.reset()))
    elif action == "modify":
        print("{}Modified task {}\n\'{}\'{}".format(
            s.theme.get_color("modify"), task.id, task.description,
            s.theme.reset()))
    elif action == "urg":
        print("{}There are more urgent tasks{}".format(
            s.theme.get_color("warn"), s.theme.reset()))
