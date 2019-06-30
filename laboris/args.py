import argparse
import sys
from laboris.smart_datetime import new

def validate_args(args, keys):
    missing = []
    for key in keys:
        if key not in args:
            missing.append(key)
    if missing:
        print_help(args['action'], False)
        print("laboris {} error: the following arguments are required: {}".format(args['action'], ', '.join(missing)))
        sys.exit(2)
    return True

def print_help(target=None, should_exit=True):
    if target is None:
        print("usage: laboris [-h|--help] [action]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system\n")
        print("-h, --help  Displays this help text")
        print("action      {add, modify, start, stop, done, undone, delete, report, sync}")
        print("            Determines the sub action to execute")
    elif target == 'add':
        print("usage: laboris add [-h|--help] [ARGS [ARGS...]]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris add - Create a new task\n")
        print("-h, --help  Displays this help text")
        print("ARGS        Arguments to add to the task that is being created. There are some\n            special tags, and if an argument does not match one of these tags,\n            it is assumed to be part of the title of the task.")
        print("              +PROJECT  will add PROJECT to the tasks projects")
        print("              @TAG      will add TAG to the tasks tags")
        print("              due:DATE  will set the due date of the task to DATE")
        print("              p:PRI     will set the priority of the task to PRI")
    elif target == 'modify':
        print("usage: laboris modify [-h|--help] UUID [ARGS [ARGS...]]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris modify - Modify an existing task\n")
        print("-h, --help  Displays this help text")
        print("UUID        The UUID of the task, this can also be reference by the task id,\n            or the task title")
        print("ARGS        Arguments to modify to the task that is being modified. There are\n            some special tags, and if an argument does not match one of these\n            tags, it is assumed to be part of the title of the task.")
        print("              +PROJECT  will add PROJECT to the tasks projects")
        print("              @TAG      will add TAG to the tasks tags")
        print("              due:DATE  will set the due date of the task to DATE")
        print("              p:PRI     will set the priority of the task to PRI")
    elif target == 'start':
        print("usage: laboris start [-h|--help] UUID [TIME]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris start - Start tracking time for an existing task\n")
        print("  Note that to start a task, it may not already be active.\n")
        print("-h, --help  Displays this help text")
        print("UUID        The UUID of the task, this can also be reference by the task id,\n            or the task title")
        print("TIME        The date/time that work started on the task. This can be a\n            relative time")
    elif target == 'stop':
        print("usage: laboris stop [-h|--help] UUID [TIME]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris stop - Start tracking time for an existing task\n")
        print("  Note that to stop a task, it must already be active.\n")
        print("-h, --help  Displays this help text")
        print("UUID        The UUID of the task, this can also be reference by the task id,\n            or the task title")
        print("TIME        The date/time that work stopped on the task. This can be a\n            relative time")
    elif target == 'done':
        print("usage: laboris done [-h|--help] UUID\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris done - Mark a pending task as completed\n")
        print("  Note that in order to mark a task as completed, it must not be active\n")
        print("-h, --help  Displays this help text")
        print("UUID        The UUID of the task, this can also be reference by the task id,\n            or the task title")
    elif target == 'undone':
        print("usage: laboris undone [-h|--help] UUID\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris undone - Mark a completed task as pending\n")
        print("-h, --help  Displays this help text")
        print("UUID        The UUID of the task")
    elif target == 'delete':
        print("usage: laboris delete [-h|--help] UUID\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris delete - Removes a task form the local and remote database\n")
        print("  Note that this is irreversible\n")
        print("-h, --help  Displays this help text")
        print("UUID        The UUID of the task")
    elif target == 'report':
        print("usage: laboris report [-h|--help]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris report - Tools to construct reports of the users tasks, and time\n")
        print("  Note this is still a WIP\n")
    elif target == 'sync':
        print("usage: laboris sync [-h|--help] [-a|--all]\n")
        print("Laboris - A CLI interface for the laboris task manager/time tracking system")
        print("Laboris sync - Manually requests a database sync\n")
        print("-h, --help       Displays this help text")
        print("-a, --all        Syncs all historical data with the database, not just the\n                 recent data")
        print("-c, --completed  Syncs all completed data with the database")


    print()
    if should_exit:
        sys.exit(0)

def parse_add():
    args = {'action': 'add', 'projects': [], 'tags': [], 'priority': 0, 'args': []}
    for arg in sys.argv[2:]:
        if arg[0] == '+':
            args['projects'].append(arg[1:])
        elif arg[0] == '@':
            args['tags'].append(arg[1:])
        elif arg.startswith('due:'):
            args['dueDate'] = new(arg[4:])
        elif arg.startswith('p:'):
            args['priority'] = int(arg[2:])
        elif arg in ('-h', '--help'):
            print_help(args['action'])
        elif 'title' not in args:
            args['title'] = arg
        else:
            args['title'] += ' ' + arg
    validate_args(args, ['title'])
    return args

def parse_modify():
    args = {'action': 'modify'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        args['uuid'] = sys.argv[2]
    for arg in sys.argv[3:]:
        if arg[0] == '+':
            if 'projects' in args:
                args['projects'].append(arg[1:])
            else:
                args['projects'] = [arg[1:]]
        elif arg[0] == '@':
            if 'tags' in args:
                args['tags'].append(arg[1:])
            else:
                args['tags'] = [arg[1:]]
        elif arg.startswith('due:'):
            args['dueDate'] = new(arg[4:])
        elif arg.startswith('p:'):
            args['priority'] = int(arg[2:])
        elif arg in ('-h', '--help'):
            print_help(args['action'])
        elif 'title' not in args:
            args['title'] = arg
        else:
            args['title'] += ' ' + arg
    validate_args(args, ['uuid'])
    return args

def parse_start():
    args = {'action': 'start'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        args['uuid'] = sys.argv[2]
    if len(sys.argv) > 3:
        if sys.argv[3] in ('-h', '--help'):
            print_help(args['action'])
        args['time'] = new(sys.argv[3])
    validate_args(args, ['uuid'])
    return args

def parse_stop():
    args = {'action': 'stop'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        args['uuid'] = sys.argv[2]
    if len(sys.argv) > 3:
        if sys.argv[3] in ('-h', '--help'):
            print_help(args['action'])
        args['time'] = new(sys.argv[3])
    validate_args(args, ['uuid'])
    return args

def parse_done():
    args = {'action': 'done'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        args['uuid'] = sys.argv[2]
    validate_args(args, ['uuid'])
    return args

def parse_undone():
    args = {'action': 'undone'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        args['uuid'] = sys.argv[2]
    validate_args(args, ['uuid'])
    return args

def parse_delete():
    args = {'action': 'delete'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        args['uuid'] = sys.argv[2]
    validate_args(args, ['uuid'])
    return args

def parse_report_list():
    args = {'action': 'report', 'report': 'list'}
    if len(sys.argv) > 3:
        if sys.argv[3] in ('-h', '--help'):
            print_help(args['action'])
        elif sys.argv[3] in ('-a', '--all', 'all'):
            args['all'] = True
    return args

def parse_report():
    args = {'action': 'report'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        elif sys.argv[2] == 'list':
            return parse_report_list()
        elif sys.argv[2] == 'detail':
            return parse_report_detail()
    validate_args(args, ['action', 'report'])
    return args

def parse_sync():
    args = {'action': 'sync'}
    if len(sys.argv) > 2:
        if sys.argv[2] in ('-h', '--help'):
            print_help(args['action'])
        elif sys.argv[2] in ('-a', '--all', 'all'):
            args['all'] = True
        elif sys.argv[2] in ('-c', '--completed', 'completed'):
            args['completed'] = True
    if len(sys.argv) > 3:
        if sys.argv[3] in ('-h', '--help'):
            print_help(args['action'])
        elif sys.argv[3] in ('-a', '--all', 'all'):
            args['all'] = True
        elif sys.argv[3] in ('-c', '--completed', 'completed'):
            args['completed'] = True
    return args

def parse_args():
    args = {'action': ''}
    if len(sys.argv) > 1:
        if sys.argv[1] == 'add':
            return parse_add()
        elif sys.argv[1] == 'modify':
            return parse_modify()
        elif sys.argv[1] == 'start':
            return parse_start()
        elif sys.argv[1] == 'stop':
            return parse_stop()
        elif sys.argv[1] == 'done':
            return parse_done()
        elif sys.argv[1] == 'undone':
            return parse_undone()
        elif sys.argv[1] == 'delete':
            return parse_delete()
        elif sys.argv[1] == 'report':
            return parse_report()
        elif sys.argv[1] == 'sync':
            return parse_sync()
        elif sys.argv[1] in ('-h', '--help'):
            print_help()
        else:
            args['task']=sys.argv[1]
    return args
