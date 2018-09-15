"""
Core modules for Laboris task manager
"""

import laboris.task as task
from laboris.config import load_config, CONFIG
from laboris.color import Attr
from laboris.argparse import parse
# from laboris.report import run_report

def main():
    load_config()
    task.load_pending()
    task.load_completed()
    # run_report()
    # print(task.PENDING_ID)
    # ret = task.get_task(input("TASK: "))
    # print(ret)
    # print(task.get_uuid(ret[1]))
    parse()
    task.save_pending()
    task.save_completed()
