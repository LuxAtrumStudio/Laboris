#!/usr/bin/python3

import argparse
import laboris.actions as action
import laboris.settings as sett
import laboris.parser as par
import os
import sys
from datetime import datetime, timedelta


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
    return False


def valid_datetime(arg):
    arg = arg.replace("@", "T")
    arg = arg.replace('/', '-')
    dmy = [
        "%d-%m-%Y", "%d-%m-%y", "%m-%d-%Y", "%m-%d-%y", "%Y-%m-%d", "%y-%m-%d",
    ]
    dmyhm = [
        "%d-%m-%YT%H:%M", "%d-%m-%yT%H:%M", "%m-%d-%YT%H:%M", "%m-%d-%yT%H:%M",
        "%Y-%m-%dT%H:%M", "%y-%m-%dT%H:%M"
    ]
    a = ["%A", "%a"]
    ahm = ["%AT%H:%M", "%AT%H:%M:%S", "%aT%H:%M", "%aT%H:%M:%S"]
    dm = ["%d-%m", "%m-%d"]
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
    if adt is not False:
        return dt.replace(year=adt.year, month=adt.month, day=adt.day)
    adt = try_date_format_set(arg, dm)
    if adt is not False:
        return dt.replace(month=adt.month, day=adt.day)
    adt = try_date_format_set(arg, hms)
    if adt is not False:
        return dt.replace(hour=adt.hour, minute=adt.minute, second=adt.second)
    adt = try_date_format_set(arg, dmyhm)
    if adt is not False:
        return adt
    adt = try_date_format_set(arg, a)
    if adt is not False:
        return adt
    adt = try_date_format_set(arg, ahm)
    if adt is not False:
        return adt
    raise argparse.ArgumentTypeError(
        "Not a valid date/time \"{0}\"".format(arg))


def valid_datetime_ref(arg):
    dt = datetime.now().replace(hour=0, minute=0, second=0)
    if arg.lower() == 'day':
        return(arg, dt)
    elif arg.lower() == 'yesterday':
        return (arg, dt - timedelta(days=1))
    elif arg.lower() == 'week':
        return (arg, dt - timedelta(days=dt.weekday()))
    elif arg.lower() == 'lastweek':
        return (arg, dt - timedelta(days=dt.weekday() + 7))
    elif arg.lower() == 'all':
        return (arg, datetime(year=1, month=1, day=1))
    elif arg.lower() == 'month':
        return (arg, dt - timedelta(days=dt.day - 1))
    elif arg.lower() == 'lastmonth':
        return (arg, dt.replace(day=1, month=dt.month - 1))
    elif arg.lower() == 'year':
        return (arg, dt.replace(day=1, month=1))
    elif arg.lower() == 'lastyear':
        return (arg, dt.replace(day=1, month=1, year=dt.year - 1))
    else:
        return (arg, valid_datetime(arg))


def valid_month(arg):
    mon = ["%b", "%B"]
    my = ["%b %Y", "%b %y", "%B %Y", "%B %y"]
    dt = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    adt = try_date_format_set(arg, mon)
    if adt is not False:
        return dt.replace(month=adt.month)
    adt = try_date_format_set(arg, my)
    if adt is not False:
        return dt.replace(month=adt.month, year=adt.year)
    raise argparse.ArgumentTypeError(
        "Not a valid month \"{0}\"".format(arg))


def set_default_subparser(self, name, args=None):
    """default subparser selection. Call after setup, just before parse_args()
    name: is the name of the subparser to call by default
    args: if set is the argument list handed to parse_args()

    , tested with 2.7, 3.2, 3.3, 3.4
    it works with 2.6 assuming argparse is installed
    """
    subparser_found = False
    existing_default = False  # check if default parser previously defined
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
                if sp_name == name:  # check existance of default parser
                    existing_default = True
        if not subparser_found:
            # If the default subparser is not among the existing ones,
            # create a new parser.
            # As this is called just before 'parse_args', the default
            # parser created here will not pollute the help output.

            if not existing_default:
                for x in self._subparsers._actions:
                    if not isinstance(x, argparse._SubParsersAction):
                        continue
                    x.add_parser(name)
                    break  # this works OK, but should I check further?

            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            if args is None:
                sys.argv.insert(1, name)
            else:
                args.insert(0, name)


def main():
    argparse.ArgumentParser.set_default_subparser = set_default_subparser
    parser = argparse.ArgumentParser(
        description="Task priority tracker, and manager.")
    parser.add_argument('--version', action='version', version="%(prog)s 2.0")
    subparsers = parser.add_subparsers(
        help="Possible actions to preform", dest="command")
    add = subparsers.add_parser('add', help="Create new task")
    add.add_argument('description', type=str,
                     nargs='+', help="Task description")
    add.add_argument('--priority', '-p', type=int,
                     default=0, help="Sets task priority")
    add.add_argument('--due', '-d', type=valid_datetime,
                     nargs='?', help="Date/Time task is due")
    add.add_argument('--tag', '-t', type=str, nargs='*', help="Task tags")
    add.add_argument('--project', '-pr', type=str,
                     nargs='*', help="Task projects")
    done = subparsers.add_parser('done', help="Complete specified task")
    done.add_argument('task', help="Task to complete")
    undone = subparsers.add_parser(
        'undone', help="Remove specified task from completed list")
    undone.add_argument('task', type=str, help="Task to un-complete")
    start = subparsers.add_parser(
        'start', help="Begin tracking time for specified task")
    start.add_argument('task', help="Task to start work on")
    start.add_argument('time', nargs='?', type=valid_datetime,
                       help="Date/Time work started on task")
    stop = subparsers.add_parser(
        'stop', help="Stop tracking time for specified task")
    stop.add_argument('task', help="Task to stop work on")
    stop.add_argument('time', nargs='?', type=valid_datetime,
                      help="Date/Time work stoped on task")
    delete = subparsers.add_parser('delete', help="Delete specified task")
    delete.add_argument('task', help='Task to delete')
    modify = subparsers.add_parser(
        'modify', help="Modify specified task entry")
    modify.add_argument('task', help='Task to modify')
    modify.add_argument('description', type=str,
                        nargs='*', help="Task description")
    modify.add_argument('--priority', '-p', type=int,
                        nargs='?', help="Sets task priority")
    modify.add_argument('--due', '-d', type=valid_datetime,
                        nargs='?', help="Date/Time task is due")
    modify.add_argument('--tag', '-t', type=str, nargs='*', help="Task tags")
    modify.add_argument('--project', '-pr', type=str,
                        nargs='*', help="Task projects")
    lis = subparsers.add_parser(
        'list', help="List information of tasks or single task")
    lis.add_argument('task', nargs='?', help="Task search string")
    lis.add_argument('--sort', nargs='?',
                     choices=["urgency", "description", "due",
                              "entry", "done", "id", "uuid",
                              "project", "tag", "status", "times",
                              "priority"],
                     help="Object to sort list by")
    lis.add_argument('--group', nargs='?',
                     choices=['due', 'all', 'pending', 'completed'],
                     default='pending', help="Shows groups of tasks")
    lis.add_argument('--format', nargs='?', type=str,
                     help="Format of task table")
    report = subparsers.add_parser(
        'report', help="Display information in formated report")
    reports = report.add_subparsers(
        help="different report formats", dest="report")
    summary = reports.add_parser('summary')
    summary.add_argument('--all', action='store_true',
                         help="Shows summary for all projects (including completed ones)")
    summary.add_argument('--clear', action='store_true',
                         help="Clears screen before printing")
    summary.add_argument('--monitor', action='store_true',
                         help="Updates result every second")
    active = reports.add_parser('active')
    active.add_argument('--clear', action='store_true',
                        help="Clears screen before printing")
    active.add_argument('--monitor', action='store_true',
                        help="Updates result every second")
    times = reports.add_parser('times')
    times.add_argument('start', nargs='?',
                       type=valid_datetime_ref, help="Datetime range begining")
    times.add_argument('stop', nargs='?',
                       type=valid_datetime_ref, help="Datetime range ending")
    times.add_argument('--group', nargs='?',
                       choices=['all', 'pending', 'completed'],
                       default='all', help="Shows groups of tasks")
    times.add_argument('--clear', action='store_true',
                       help="Clears screen before printing")
    times.add_argument('--monitor', action='store_true',
                       help="Updates result every second")
    burn = reports.add_parser('burndown')
    burn.add_argument('--clear', action='store_true',
                      help="Clears screen before printing")
    burn.add_argument('--monitor', action='store_true',
                      help="Updates result every second")
    burn.add_argument('--trim', action='store_true',
                      help="Removes un-tracked days on either end of tracked days")
    burn.add_argument('start', nargs='?',
                      type=valid_datetime_ref, help="Datetime range begining")
    burn.add_argument('stop', nargs='?',
                      type=valid_datetime_ref, help="Datetime range ending")
    graph = reports.add_parser('graph')
    graph.add_argument('--group', nargs='?',
                       choices=['all', 'pending', 'completed'],
                       default='all', help="Shows groups of tasks")
    graph.add_argument('--clear', action='store_true',
                       help="Clears screen before printing")
    graph.add_argument('--monitor', action='store_true',
                       help="Updates result every second")
    graph.add_argument('--trim', action='store_true',
                       help="Removes un-tracked days on either end of tracked days")
    graph.add_argument('--trim-all', action='store_true',
                       help="Removes all un-tracked days")
    graph.add_argument('start', nargs='?',
                       type=valid_datetime_ref, help="Datetime range begining")
    graph.add_argument('stop', nargs='?',
                       type=valid_datetime_ref, help="Datetime range ending")
    cal = reports.add_parser('calendar',
                             help="Displays upcoming and past tasks in a calendar format")
    cal.add_argument('start', nargs='?', type=valid_month,
                     help="Number of month ago to start display")
    cal.add_argument('stop', nargs='?', type=valid_month,
                     help="Number of month ago to start display")
    cal.add_argument('--clear', action='store_true',
                     help="Clears screen before printing")
    cal.add_argument('--monitor', action='store_true',
                     help="Updates result every second")
    parser.set_default_subparser('list')
    args = parser.parse_args()
    sett.init()
    action.run_action(args)
    sett.term()


if __name__ == "__main__":
    main()
