#!/usr/bin/env python3

from pprint import pprint

import urllib.request
import urllib.error
import sys
import os
import datetime
import argparse
import subprocess
import json
from configparser import ConfigParser
from math import exp, log

CONFIG = None
CONFIG_DIR = './'


def set_default_subparser(self, name, args=None, positional_args=0):
    subparser_found = False
    for arg in sys.argv[1:]:
        if arg in ['-h', '--help']:
            break
    else:
        for x in self._subparsers._actions:
            if not isinstance(x, argparse._SubParsersAction):
                continue
            for sp_name in x._name_parser_map.keys():
                if sp_name in sys.argv[1:]:
                    subparser_found = True
        if not subparser_found:
            if args is None:
                sys.argv.insert(len(sys.argv) - positional_args, name)
            else:
                args.insert(len(args) - positional_args, name)


argparse.ArgumentParser.set_default_subparser = set_default_subparser


def try_date_fmt(arg, fmt):
    try:
        dt = datetime.datetime.strptime(arg, fmt)
        now = datetime.datetime.now()
        cdt = datetime.datetime.now().replace(hour=0,
                                              minute=0,
                                              second=0,
                                              microsecond=0)
        if (fmt == '%A' and arg in ('sunday', 'monday', 'tuesday', 'wednesday',
                                    'thursday', 'friday', 'saturday')) or (
                                        (fmt == '%a')
                                        and arg in ('sun', 'mon', 'tue', 'wed',
                                                    'thu', 'fri', 'sat')):
            while cdt.strftime(fmt).lower() != arg:
                cdt += datetime.timedelta(days=1)
        elif (fmt.startswith('%A@') and arg.split('@')[0] in
              ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
               'friday', 'saturday')) or (
                   fmt.startswith('%a@') and arg.split('@')[0] in
                   ('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat')):
            while cdt.strftime(fmt.split('@')[0]).lower() != arg.split('@')[0]:
                cdt += datetime.timedelta(days=1)
        elif '%A' in fmt or '%a' in fmt:
            return None

        if '%y' in fmt or '%Y' in fmt:
            cdt = cdt.replace(year=dt.year)
        if '%m' in fmt:
            cdt = cdt.replace(month=dt.month)
        if '%d' in fmt:
            cdt = cdt.replace(day=dt.day)
        if '%H' in fmt:
            if now.date() == cdt.date() and (
                (dt.hour * 3600 + dt.minute * 60 + dt.second) <
                (now.hour * 3600 + now.minute * 60 + now.second)):
                cdt = cdt.replace(hour=dt.hour + 12)
            else:
                cdt = cdt.replace(hour=dt.hour)
        elif '%I' in fmt:
            cdt = cdt.replace(hour=dt.hour)
        if '%M' in fmt:
            cdt = cdt.replace(minute=dt.minute)
        if '%S' in fmt:
            cdt = cdt.replace(second=dt.second)
        return cdt
    except ValueError as err:
        return None


def datetime_ref(arg):
    arg = arg.lower().replace('/', '-').replace('t', '@')
    if arg[0] == '@':
        arg = 't' + arg[1:]
    formats = [
        "%d-%m-%Y@%H:%M:%S", "%d-%m-%Y@%H:%M", "%d-%m-%Y@%H",
        "%m-%d-%Y@%H:%M:%S", "%m-%d-%Y@%H:%M", "%m-%d-%Y@%H",
        "%d-%m-%y@%H:%M:%S", "%d-%m-%y@%H:%M", "%d-%m-%y@%H", "%d-%m-%Y",
        "%m-%d-%Y", "%d-%m-%y", "%m-%d-%y", "%d-%m@%H:%M:%S", "%d-%m@%H:%M",
        "%d-%m@%H", "%m-%d@%H:%M:%S", "%m-%d@%H:%M", "%m-%d@%H", "%d-%m",
        "%m-%d", "%Y", "%d@%H:%M:%S", "%d@%H:%M", "%d@%H", "%d", "%H:%M:%S",
        "%H:%M", "%d-%m-%Y@%I:%M:%S%p", "%d-%m-%Y@%I:%M%p", "%d-%m-%Y@%I%p",
        "%m-%d-%Y@%I:%M:%S%p", "%m-%d-%Y@%I:%M%p", "%m-%d-%Y@%I%p",
        "%d-%m-%y@%I:%M:%S%p", "%d-%m-%y@%I:%M%p", "%d-%m-%y@%I%p",
        "%d-%m@%I:%M:%S%p", "%d-%m@%I:%M%p", "%d-%m@%I%p", "%m-%d@%I:%M:%S%p",
        "%m-%d@%I:%M%p", "%m-%d@%I%p", "%d@%I:%M:%S%p", "%d@%I:%M%p",
        "%d@%I%p", "%I:%M:%S%p", "%I:%M%p", "%A@%H:%M:%S", "%A@%H:%M", "%A@%H",
        "%A", "%a@%H:%M:%S", "%a@%H:%M", "%a@%H", "%a", "%A@%I:%M:%S%p",
        "%A@%I:%M%p", "%A@%I%p", "%a@%I:%M:%S%p", "%a@%I:%M%p", "%a@%I%p"
    ]
    dt = None
    i = 0
    while dt is None and i < len(formats):
        dt = try_date_fmt(arg, formats[i])
        i += 1
    if dt is None:
        dt = datetime.datetime.now().replace(microsecond=0)
        delim = ' ' if ' ' in arg else ','
        for opt in arg.split(delim):
            if opt[0] == '+':
                if opt[-1] == 'd':
                    dt += datetime.timedelta(days=int(opt[1:-1]))
                elif opt[-1] == 'h':
                    dt += datetime.timedelta(seconds=3600 * int(opt[1:-1]))
                elif opt[-1] == 'm':
                    dt += datetime.timedelta(seconds=60 * int(opt[1:-1]))
                elif opt[-1] == 's':
                    dt += datetime.timedelta(seconds=int(opt[1:-1]))
                else:
                    return None
            elif opt[0] == '_' or opt[0] == '-':
                if opt[-1] == 'd':
                    dt -= datetime.timedelta(days=int(opt[1:-1]))
                elif opt[-1] == 'h':
                    dt -= datetime.timedelta(seconds=3600 * int(opt[1:-1]))
                elif opt[-1] == 'm':
                    dt -= datetime.timedelta(seconds=60 * int(opt[1:-1]))
                elif opt[-1] == 's':
                    dt -= datetime.timedelta(seconds=int(opt[1:-1]))
                else:
                    return None
            else:
                return None
    return dt


def datediff(a, b):
    diff = a - b
    return diff.days + (diff.seconds / 86400)


def date_abbrev(lhs, rhs):
    output = ""
    if isinstance(lhs, int):
        lhs = timestamp(lhs)
    if isinstance(rhs, int):
        rhs = timestamp(rhs)
    if rhs is None:
        return output
    if lhs > rhs:
        diff = lhs - rhs
        output += '-'
    else:
        diff = rhs - lhs
    if abs(diff.days) > 7:
        output += str(int(diff.days / 7)) + "w"
    elif abs(diff.days) > 0:
        output += str(int(diff.days)) + 'd'
    elif abs(diff.seconds) > 3600:
        output += str(int(diff.seconds / 3600)) + "h"
    elif abs(diff.seconds) > 60:
        output += str(int(diff.seconds / 60)) + "m"
    elif abs(diff.seconds) > 0:
        output += str(diff.seconds) + "s"
    else:
        output = "NOW"
    return output


def timestamp(ts):
    return datetime.datetime.fromtimestamp(float(ts) / 1000)


def execute_backlog():
    if os.path.exists(CONFIG_DIR + 'requests.txt'):
        with open(CONFIG_DIR + 'requests.txt', 'r') as backlog:
            requests = [x.strip().split('	') for x in backlog.readlines()]
        for req in requests:
            if req[0] == 'POST':
                urllib.request.urlopen(urllib.request.Request(
                    req[1], headers={'Content-Type': 'application/json'}),
                                       req[2].encode('utf-8'),
                                       timeout=1)
        os.remove(CONFIG_DIR + 'requests.txt')


def execute_post_request(url, data):
    try:
        res = urllib.request.urlopen(urllib.request.Request(
            url, headers={'Content-Type': 'application/json'}),
                                     json.dumps(data).encode('utf-8'),
                                     timeout=1)
        execute_backlog()
        return json.loads(res.read().decode('utf-8'))
    except:
        with open(CONFIG_DIR + 'requests.txt', 'a+') as backlog:
            backlog.write("{}	{}	{}\n".format('POST', url, json.dumps(data)))


def execute_get_request(url):
    res = urllib.request.urlopen(url)
    return json.loads(res.read().decode('utf-8'))


def load_config():
    global CONFIG
    global CONFIG_DIR
    if os.path.exists('laboris.ini'):
        CONFIG_DIR = './'
    elif os.path.exists('~/.laboris.ini'):
        CONFIG_DIR = '~/'
    elif os.path.exists('~/.laboris/laboris.ini'):
        CONFIG_DIR = '~/.laboris/'
    elif os.path.exists('~/.config/laboris/laboris.ini'):
        CONFIG_DIR = '~/.config/laboris/'
    CONFIG = ConfigParser()
    CONFIG.read(CONFIG_DIR + 'laboris.ini')


def parse_args():
    for i in range(len(sys.argv)):
        if sys.argv[i][0] == '-' and 49 <= ord(sys.argv[i][1]) <= 57:
            sys.argv[i] = '_' + sys.argv[i][1:]
    parser = argparse.ArgumentParser('laboris')
    sub = parser.add_subparsers(dest='cmd')
    add = sub.add_parser('add', help='Add new task')
    add.add_argument('title', nargs='+', help='Title for the task')
    add.add_argument('--pri',
                     type=int,
                     nargs='?',
                     default=5,
                     help='Priority of the task 1-5')
    add.add_argument('--hidden',
                     action='store_true',
                     help='Hide task in reports (useful for meta tasks)')
    add.add_argument('-t',
                     '--tag',
                     nargs='?',
                     default=[],
                     help='Tags for the task')
    add.add_argument('-p',
                     '--parent',
                     nargs='?',
                     default=[],
                     help='Parent tasks for the task')
    add.add_argument('-c',
                     '--child',
                     nargs='?',
                     default=[],
                     help='Child tasks for the task')
    add.add_argument('--due',
                     nargs='?',
                     type=datetime_ref,
                     help='Time the task is due')

    modify = sub.add_parser('modify', help='Modify existing task')
    modify.add_argument('id', type=str, help='Task id')
    modify.add_argument('title', nargs='*', help='Title for the task')
    modify.add_argument('--pri',
                        type=int,
                        nargs='?',
                        default=5,
                        help='Priority of the task 1-5')
    modify.add_argument('--hidden',
                        action='store_true',
                        help='Hide task in reports (useful for meta tasks)')
    modify.add_argument('-t', '--tag', nargs='?', help='Tags for the task')
    modify.add_argument('-p',
                        '--parent',
                        nargs='?',
                        help='Parent tasks for the task')
    modify.add_argument('-c',
                        '--child',
                        nargs='?',
                        help='Child tasks for the task')
    modify.add_argument('--due',
                        nargs='?',
                        type=datetime_ref,
                        help='Time the task is due')

    done = sub.add_parser('done', help='Mark task as compleated/inactive')
    done.add_argument('id', type=str, help='Task id')

    start = sub.add_parser('start', help='Start work on a task')
    start.add_argument('id', type=str, help='Task id')
    start.add_argument('time',
                       type=datetime_ref,
                       help='Time the work was started')
    stop = sub.add_parser('stop', help='Stop work on a task')
    stop.add_argument('id', type=str, help='Task id')
    stop.add_argument('time',
                      type=datetime_ref,
                      help='Time the work was stopped')

    sync = sub.add_parser(
        'sync',
        help="Sync data to and from the server, can be configured to run after"
        " a loss of connection")
    sync.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='Syncs all data, don\'t run this, it can take a long time')
    sync.add_argument(
        '-s',
        '--since',
        type=datetime_ref,
        default=timestamp(int(CONFIG['REMOTE']['synced'])),
        help='Syncs all data, that has been modifed since this time')

    config = sub.add_parser('config', help="Manage Laboris configuration file")
    config.add_argument('--url',
                        type=str,
                        help='Set the url of the remote host')
    config.add_argument('--user',
                        type=str,
                        help='Set the user for the remote host')

    report = sub.add_parser('report', help="View task reports")
    report.add_argument('args', nargs='*')

    parser.set_default_subparser('report')
    return parser.parse_args()


def calc_urg_due(body):
    if 'dueDate' not in body or body['dueDate'] is None:
        return 0.0
    due = datediff(timestamp(body['dueDate']), datetime.datetime.now())
    age = datediff(timestamp(body['dueDate']), timestamp(body['entryDate']))
    k = log(81) / age
    x0 = log(1 / 9) / -k
    return 1.0 / (1 + exp(-k + (due + x0)))


def calc_urg(body):
    urg = 0.0
    urg += abs(
        float(CONFIG['URGENCY']['age']) *
        datediff(timestamp(body['entryDate']), datetime.datetime.now()))
    urg += abs(float(CONFIG['URGENCY']['due']) * calc_urg_due(body))
    urg += abs(float(CONFIG['URGENCY']['parent']) * len(body['parents']))
    urg += abs(float(CONFIG['URGENCY']['child']) * len(body['children']))
    urg += abs(float(CONFIG['URGENCY']['tag']) * len(body['tags']))
    urg += abs(
        float(CONFIG['URGENCY']['active']
              ) if body['times'] and len(body['times'][-1]) == 1 else 0.0)
    urg += (float(CONFIG['URGENCY']['priority']) * body['priority'] +
            float(CONFIG['URGENCY']['priority offset']))
    if body['priority'] == 0 or body['status'] != 'active':
        urg = 0.0
    return urg


def sort_by_urg(tasks):
    return sorted(tasks, key=lambda x: calc_urg(x), reverse=True)


def parse_fmt(fmt):
    fmt = fmt.split(' ')
    fmt = [x.strip('{}').split(':') for x in fmt]
    res = []
    for kv in fmt:
        if len(kv) == 1:
            res.append((kv[0], {}))
            continue
        key, val = kv
        idx = 0
        attr = {}
        if val[idx] in '<^>':
            attr['align'] = val[idx]
            idx += 1
        if idx < len(val) and val[idx] in '0123456789':
            attr['width'] = ''
            while idx < len(val) and val[idx] in '0123456789':
                attr['width'] += val[idx]
                idx += 1
            attr['width'] = int(attr['width'])
        if idx < len(val) and val[idx] == '.':
            attr['perc'] = ''
            idx += 1
            while idx < len(val) and val[idx] in '0123456789':
                attr['perc'] += val[idx]
                idx += 1
            attr['perc'] = int(attr['perc'])
        if idx < len(val) and val[idx] in '-+':
            attr['wrap'] = val[idx]
            idx += 1
        if idx < len(val):
            attr['type'] = val[idx:]
        res.append((key, attr))
    return res


def fmt_entry(attr, body):
    fmted = '{' + attr[0]
    if attr[1]:
        fmted += ':'
        if 'align' in attr[1]:
            fmted += attr[1]['align']
        if 'width' in attr[1]:
            fmted += str(attr[1]['width'])
        if 'perc' in attr[1]:
            fmted += '.' + str(attr[1]['perc'])
        if 'type' in attr[1]:
            fmted += attr[1]['type']
    fmted += '}'
    fmted = fmted.format(**body)
    if 'width' in attr[1] and len(
            fmted) > attr[1]['width'] and 'wrap' in attr[1]:
        if attr[1]['wrap'] == '-':
            if attr[1]['width'] >= 10:
                return fmted[:attr[1]['width'] - 3] + '...'
            else:
                return fmted[:attr[1]['width']]
        elif attr[1]['wrap'] == '+':
            words = fmted.split()
            fmted = ['']
            for word in words:
                if len(fmted[-1] + ' ' + word) >= attr[1]['width'] - 1:
                    fmted.append('')
                fmted[-1] += ' ' + word
            fmted = []
            for i, ln in enumerate(fmted):
                ln = ln[1:]
                if 'align' in attr[1] and attr[1]['align'] == '>':
                    pre = ' ' * (attr[1]['width'] - len(ln))
                    post = ''
                elif 'align' in attr[1] and attr[1]['align'] == '^':
                    pre = ' ' * ((attr[1]['width'] - len(ln)) / 2)
                    post = ' ' * ((attr[1]['width'] - len(ln)) / 2)
                else:
                    post = ' ' * (attr[1]['width'] - len(ln))
                    pre = ''
                fmted.append(pre + ln + post)
    return fmted


def fmt_task(body, fmt):
    body = {
        **body, 'id':
        body['_id'],
        'id-short':
        body['_id'][:4],
        'due-short':
        date_abbrev(datetime.datetime.now(), timestamp(body['dueDate']))
        if body['dueDate'] else '',
        'parents-count':
        len(body['parents']),
        'children-count':
        len(body['children']),
        'tag-count':
        len(body['tags']),
        'tags':
        ' '.join(body['tags']),
        'urg':
        calc_urg(body)
    }
    res = {}
    for key in fmt:
        res[key[0]] = fmt_entry(key, body)
    return res


def print_task_short(tasks):
    fmt = parse_fmt(CONFIG['REPORTS']['list format'])
    data = [fmt_task(x, fmt) for x in tasks]
    pprint(data)


def action_add(args):
    payload = {
        'title': '',
        'priority': args.pri,
        'hidden': args.hidden,
        'tags': args.tag,
        'parents': args.parent,
        'children': args.child,
        'dueDate': args.due.timestamp() * 1000 if args.due else None
    }
    for arg in args.title:
        if arg[0] == '@':
            payload['tags'].append(arg[1:])
        elif arg[0] == '+':
            payload['parents'].append(arg[1:])
        elif arg[0] == '=':
            payload['children'].append(arg[1:])
        elif arg.startswith('p:'):
            payload['priority'] = int(arg[2:])
        elif arg.startswith('due:'):
            payload['dueDate'] = datetime_ref(arg[4:]).timestamp() * 1000
        else:
            payload['title'] += ' ' + arg
    payload['title'] = payload['title'][1:]
    execute_post_request(CONFIG['REMOTE']['host'] + '/api/', payload)


def action_report(args):
    tasks = execute_get_request(CONFIG['REMOTE']['host'] + '/api/')
    tasks = sort_by_urg(tasks)
    print_task_short(tasks)


def main():
    load_config()
    args = parse_args()
    if args.cmd == 'add':
        action_add(args)
    # if args.cmd == 'modify':
    #     action_add(args)
    # if args.cmd == 'done':
    #     action_add(args)
    # if args.cmd == 'start':
    #     action_add(args)
    # if args.cmd == 'stop':
    #     action_add(args)
    # if args.cmd == 'sync':
    #     action_add(args)
    # if args.cmd == 'config':
    #     action_add(args)
    if args.cmd == 'report':
        action_report(args)


if __name__ == "__main__":
    main()
