import sys
import printer
import task
from color import fg, bg, attr, stylize
from datetime import date, time, datetime


def attempt_date(string, fmt):
    try:
        print(datetime.now())
        print(string, fmt)
        dt = datetime.strptime(string, fmt)
        print(dt)
    except ValueError:
        return False
    return dt


def get_date(arg):
    if attempt_date(arg, "%d-%m-%y") is not False:
        return attempt_date(arg, "%d-%m-%y")
    elif attempt_date(arg, "%d-%m-%Y") is not False:
        return attempt_date(arg, "%d-%m-%Y")
    elif attempt_date(arg, "%H:%M") is not False:
        return attempt_date(arg, "%H:%M")
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
            print(arg)
            new_task.due = get_date(arg)
            print(new_task.due)
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
    print("{}Added Task: {}{}".format(fg('green'), new_task.id, attr('reset')))
    print("{}\"{}\"{}".format(fg('green'), new_task.description, attr('reset')))
    return True


def parse_cmd(args, pending, done):
    if args[0] == "add" and add_task(args[1:], pending) is True:
        return True
    return False


def parse_args(pending, done):
    args = sys.argv[1:]
    if len(args) == 0:
        printer.print_set(pending, "id|entry;abbr|project|due;abbr|description|urg")
        print()
    elif parse_cmd(args, pending, done) is False:
        printer.print_set(pending, "id|entry;abbr|project|due;abbr|description|urg")
        print()
        print(stylize("Invalid command: \"{}\"", [fg('red'), attr('bold')]).format(' '.join(args)))
