import argparse
from laboris.smart_datetime import new


def parse_args():
    parser = argparse.ArgumentParser('laboris')
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
