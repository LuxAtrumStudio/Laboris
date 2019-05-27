import argparse
import sys
from laboris.smart_datetime import new

def set_default_subparser(self, name, args=None, positional_args=0):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:  # global help if no subparser
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            # insert default in last position before global positional
            # arguments, this implies no global options are specified after
            # first positional argument
            if args is None:
                sys.argv.insert(len(sys.argv) - positional_args, name)
            else:
                args.insert(len(args) - positional_args, name)

argparse.ArgumentParser.set_default_subparser = set_default_subparser

def parse_args():
    parser = argparse.ArgumentParser('laboris')
    parser.add_argument('task', nargs='?', help="Task to list detail of")
    sub_parsers = parser.add_subparsers(help="laboris actions", dest='action')
    add = sub_parsers.add_parser('add', help="adds new task")
    add.add_argument('title', type=str, help='title of task')
    add.add_argument('--pri', default=0, type=int, help='priority of task')
    add.add_argument(
        '-p',
        '--project',
        default=[],
        type=str,
        nargs='*',
        help='projects task applies to')
    add.add_argument(
        '-t', '--tag', default=[], type=str, nargs='*', help='tags for task')
    add.add_argument(
        '--due', default=None, type=new, nargs='?', help='due date for task')
    add.add_argument('args', type=str, nargs='*', help='additional arguments')
    mod = sub_parsers.add_parser('modify', help='modify existing task')
    mod.add_argument('uuid', type=str, help='uuid of task')
    mod.add_argument('title', type=str, nargs='?', help='title of task')
    mod.add_argument('-p', default=0, type=int, help='priority of task')
    mod.add_argument('-g', type=str, nargs='*', help='projects task applies to')
    mod.add_argument('-t', type=str, nargs='*', help='tags for task')
    mod.add_argument('--due', type=new, nargs='?', help='due date for task')
    mod.add_argument('args', type=str, nargs='*', help='additional arguments')
    start = sub_parsers.add_parser('start', help='start a task')
    start.add_argument('uuid', type=str, help='uuid of task')
    start.add_argument('time', type=new, nargs='?', help='time of task start')
    stop = sub_parsers.add_parser('stop', help='stop a task')
    stop.add_argument('uuid', type=str, help='uuid of task')
    stop.add_argument('time', type=new, nargs='?', help='time of task stop')
    done = sub_parsers.add_parser('done', help='mark a task as completed')
    done.add_argument('uuid', type=str, help='uuid of task')
    undone = sub_parsers.add_parser('undone', help='mark a task as pending')
    undone.add_argument('uuid', type=str, help='uuid of task')
    done = sub_parsers.add_parser('delete', help='delete a task')
    done.add_argument('uuid', type=str, help='uuid of task')
    report = sub_parsers.add_parser('report', help='generate report data')
    parser.set_default_subparser('report')
    args = parser.parse_args()
    if args.action in ('add', 'mod'):
        for arg in args.args:
            if arg[0] == '+':
                args.project.append(arg[1:])
            elif arg[0] == '@':
                args.tag.append(arg[1:])
            elif arg.startswith('due:'):
                args.due = new(arg[4:])
            elif arg.startswith('p:'):
                args.pri= int(arg[2:])
    return args
