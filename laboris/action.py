"""
Reports core structure for Laboris project
"""

from laboris.reports.list import list_report

from laboris.actions.detail import detail_action
from laboris.actions.task import start_action, stop_action, done_action, undone_action, modify_action, delete_action

def run_report(report = None, task=None, args = []):
    if report is None or report.lower() == "list":
        list_report(args)

def run_task_action(action = None, task = None, args = []):
    if action is None or action.lower() == "detail":
        detail_action(task, args)
    elif action == 'start':
        start_action(task, args)
    elif action == 'stop':
        stop_action(task, args)
    elif action == 'done':
        done_action(task, args)
    elif action == 'undone':
        undone_action(task, args)
    elif action == 'modify':
        modify_action(task, args)
    elif action == 'delete':
        delete_action(task, args)


def run_action(action = None, task = None, args = []):
    if (action is None and task is None) or (action is not None and action in ('list')):
        run_report(action, task, args)
    elif (action is None and task is not None) or (action is not None and action in ('detail', 'start', 'stop', 'done', 'undone', 'modify', 'delete')):
        run_task_action(action, task, args)
    else:
        print(action, task, args)
