import sys
import printer
import task
import interval
from color import fg, bg, attr, stylize
from datetime import date, time, datetime, timedelta


def attempt_date(string, fmt):
    try:
        dt = datetime.strptime(string, fmt)
        if fmt == "%A":
            cdt = datetime.now()
            string = string.title()
            while cdt.strftime("%A") != string:
                cdt += timedelta(days=1)
            dt = dt.replace(year=cdt.year, month=cdt.month, day=cdt.day)
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

    dmy = ["%d-%m-%Y", "%d-%m-%y", "%m-%d-%Y", "%m-%d-%y", "%Y-%m-%d", "%y-%m-%d", "%d/%m/%Y", "%d/%m/%y", "%m/%d/%Y",
           "%m/%d/%y", "%Y/%m/%d", "%y/%m/%d"]
    dmyhm = ["%d-%m-%YT%H:%M", "%d-%m-%yT%H:%M", "%m-%d-%YT%H:%M", "%m-%d-%yT%H:%M", "%Y-%m-%dT%H:%M", "%y-%m-%dT%H:%M",
             "%d/%m/%YT%H:%M", "%d/%m/%yT%H:%M", "%m/%d/%YT%H:%M", "%m/%d/%yT%H:%M", "%Y/%m/%dT%H:%M", "%y/%m/%dT%H:%M"]
    a = ["%A"]
    ahm = ["%AT%H:%M", "%AT%H:%M:%S"]
    dm = ["%d-%m", "%m-%d", "%d/%m", "%m/%d"]
    hms = ["%H:%M", "%H.%M", "%H:%M:%S", "%H.%M.%S"]

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
    print(stylize("Invalid date format: \"{}\"", [fg('red'), attr('bold')]).format(arg))
    return datetime.now()


def add_task(args, pending):
    new_task = task.Task()
    new_task.entry_date = datetime.now()
    if len(args) == 0:
        return False
    for arg in args:
        if arg.startswith("p:") or arg.startswith("priority:"):
            arg = arg.split(':')[1]
            new_task.priority = int(arg)
        elif arg.startswith("due:"):
            arg = arg[4:]
            new_task.due_date = get_date(arg)
        elif arg.startswith("+"):
            arg = arg[1:]
            new_task.project.append(arg)
        elif arg.startswith("@"):
            arg = arg[1:]
            new_task.tag.append(arg)
        else:
            new_task.description += arg + ' '

    if new_task.description is not None:
        new_task.description = new_task.description[:-1]
    new_task.calculate_urgency()
    printer.print_task(new_task)
    pending.append(new_task)
    print("{}Added Task: {}{}".format(fg('green'), new_task.id, attr('reset')))
    print("{}\"{}\"{}".format(fg('green'), new_task.description, attr('reset')))
    return True


def modify_task(index, args, pending, done):
    mod_des = False
    mod_pro = False
    mod_tag = False
    for arg in args:
        if arg.startswith("p:") or arg.startswith("priority:"):
            arg = arg.split(':')[1]
            pending[index].priority = int(arg)
        elif arg.startswith("due:"):
            arg = arg[4:]
            pending[index].due_date = get_date(arg)
        elif arg.startswith("+"):
            if mod_pro is False:
                mod_pro = True
                pending[index].project = list()
            arg = arg[1:]
            pending[index].project.append(arg)
        elif arg.startswith("@"):
            if mod_tag is False:
                mod_tag = True
                pending[index].tag = list()
            arg = arg[1:]
            pending[index].tag.append(arg)
        else:
            if mod_des is False:
                mod_des = True
                pending[index].description = str()
            pending[index].description += arg + ' '

    if mod_des is True:
        pending[index].description = pending[index].description[:-1]

    pending[index].calculate_urgency()
    print("{}Modified Task: {}{}".format(fg('green'), pending[index].id, attr('reset')))
    print("{}\"{}\"{}".format(fg('green'), pending[index].description, attr('reset')))


def complete_task(index, pending, done):
    pending[index].done_date = datetime.now()
    done.append(pending[index])
    print("{}Completed Task: {}{}".format(fg('yellow'), index, attr('reset')))
    print("{}\"{}\"{}".format(fg('yellow'), pending[index].description, attr('reset')))
    del pending[index]


def delete_task(index, pending, done):
    print("{}Deleted Task: {}{}".format(fg('red'), index, attr('reset')))
    print("{}\"{}\"{}".format(fg('red'), pending[index].description, attr('reset')))
    del pending[index]


def start_interval(index, pending):
    if pending[index].active is False:
        pending[index].times.append(interval.Interval())
        print("{}Starting task {}".format(fg('yellow'), index + 1, attr('reset')))
        print("{}At: {}".format(fg('yellow'), pending[index].times[-1].print_start(True), attr('reset')))
    else:
        print("{}Task has already started: {}{}".format(fg('red'), index + 1, attr('reset')))
        print("{}\"{}\"{}".format(fg('red'), pending[index].description, attr('reset')))


def end_interval(index, pending):
    if pending[index].active is True:
        pending[index].times[-1].stop()
        print("{}Stopping task {}".format(fg('yellow'), index + 1, attr('reset')))
        print("{}At: {}".format(fg('yellow'), pending[index].times[-1].print_end(True), attr('reset')))
        print("{}{} -> {}{}".format(fg('yellow'), pending[index].times[-1].print_start(True),
                                    pending[index].times[-1].print_end(True), attr('reset')))
        print("{}Total duration: {}{}".format(fg('yellow'), pending[index].times[-1].print_duration(True),
                                              attr('reset')))
    else:
        print("{}Task is not active: {}{}".format(fg('red'), index + 1, attr('reset')))
        print("{}\"{}\"{}".format(fg('red'), pending[index].description, attr('reset')))


def parse_cmd(args, pending, done):
    if args[0] == "add" and add_task(args[1:], pending) is True:
        return True
    return False


def parse_task_id_cmd(args, pending, done):
    if args[0].isdigit() is True and int(args[0]) - 1 < len(pending):
        if len(args) == 1:
            printer.print_task(pending[int(args[0]) - 1])
        else:
            if args[1] == "done":
                complete_task(int(args[0]) - 1, pending, done)
            elif args[1] == "delete":
                delete_task(int(args[0]) - 1, pending, done)
            elif args[1] == "modify":
                modify_task(int(args[0]) - 1, args[2:], pending, done)
            elif args[1] == "start":
                start_interval(int(args[0]) - 1, pending)
            elif args[1] == "stop":
                end_interval(int(args[0]) - 1, pending)
        return True
    elif args[0].isdigit() is True and int(args[0]) - 1 >= len(pending):
        print(stylize("Task ID \'{}\' is out of range", [fg('red'), attr('bold')]).format(args[0]))
    return False


def parse_list(args, pending, done):
    t_set = list()
    i_set = 0
    fmt = str()
    if "all" in args:
        i_set = 1
        t_set = pending + done
        args.remove("all")
    elif "completed" in args:
        i_set = 2
        t_set = done
        args.remove("completed")
    elif "pending" in args:
        i_set = 0
        t_set = pending
        args.remove("pending")
    else:
        t_set = pending
    for arg in args:
        fmt += arg + '|'
    if fmt == "" and i_set == 0:
        fmt = "id|entry;abbr|project|due;abbr|description|urg"
    elif fmt == "" and i_set == 1:
        fmt = "id|st|uuid;short|age;abbr|done;abbr|p|project|due;date|description"
    elif fmt == "" and i_set == 2:
        fmt = "uuid;short|entry;date|done;date|age;abbr|p|project|due;date|description"
    else:
        fmt = fmt[:-1]
    printer.print_set(t_set, fmt)
    return True


def parse_args(pending, done):
    args = sys.argv[1:]
    if len(args) == 0:
        printer.print_set(pending, "id|entry;abbr|project|due;abbr|description|urg")
        print()
    elif parse_cmd(args, pending, done) is False and parse_task_id_cmd(args, pending, done) is False and parse_list(args, pending, done) is False:
        printer.print_set(pending, "id|entry;abbr|project|due;abbr|description|urg")
        print()
        print(stylize("Invalid command: \"{}\"", [fg('red'), attr('bold')]).format(' '.join(args)))
