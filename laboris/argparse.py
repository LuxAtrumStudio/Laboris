"""
Argument parsing module for Laboris
"""

import sys

import laboris.task
import laboris.color
from laboris.config import CONFIG
from laboris.action import run_action


def help():
    print("Usage: laboris TASK [action [options]]")
    print("       laboris REPORT")
    print("Laboris Task Manager(CLI) V2.0")
    print()
    print("  -h, --help     show list of command line options")


def parse():
    task_actions = [
        'detail', 'start', 'stop', 'done', 'undone', 'modify', 'delete'
    ]
    non_task_actions = ['add', 'create', 'new']
    reports = [
        'list', 'active', 'calendar', 'graph', ' burndown', 'wpd', 'times',
        'project', 'summary', 'cal'
    ]
    require_ref = False
    action = None
    task = None
    args = []
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
        exit(0)
    for arg in sys.argv[1:]:
        if arg.lower() in reports:
            action = arg.lower()
        elif arg.lower() in non_task_actions:
            action = arg.lower()
        elif arg.lower() in task_actions:
            action = arg.lower()
            require_ref = task is None
        elif action is None or require_ref is True:
            task = laboris.task.get_task(arg)
            require_ref = False
        else:
            args.append(arg)
    if require_ref is True:
        print(
            laboris.color.Attr("Error: \"{}\" requires a task".format(action),
                               CONFIG.get_color('msg.error')))
    else:
        run_action(action, task, args)
    return None
