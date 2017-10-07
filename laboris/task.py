"""This is the task module that contains task and time data"""

import time
import json
import itertools
import collections
import uuid
from datetime import datetime, date, time


class Task:
    def __init__(self, _desc=str(), _project=list(), _tag=(), _priority=int(), _entry=None, _due=None, _done=None):
        self.description = _desc
        self.project = _project
        self.tag = _tag
        self.uuid = uuid.uuid1()
        self.priority = _priority
        self.urgency = float()
        if _entry is None:
            self.entry_date = datetime(1, 1, 1)
        else:
            self.entry_date = _entry
        if _due is None:
            self.due_date = datetime(1, 1, 1)
        else:
            self.due_date = _due
        if _done is None:
            self.done_date = datetime(1, 1, 1)
        else:
            self.done_date = _done

    def __repr__(self):
        return str("THIS IS A TASK!\n")

    def __format__(self, format_spec):
        return format_spec

    def print_project(self, index=None):
        if index is None:
            output = str()
            for p in self.project:
                output += p + " "
            return output
        if len(self.project) > index:
            return self.project[index]
        else:
            return str()

    def print_tag(self, index=None):
        if index is None:
            output = str()
            for t in self.tag:
                output += t + " "
            return output
        if len(self.tag) > index:
            return self.tag[index]
        else:
            return str()

    def print_date_abbr(self, lhs, rhs):
        output = str()
        if lhs > rhs:
            diff = lhs - rhs
            output += "-"
        else:
            diff = rhs - lhs
        if abs(diff.days) > 7:
            output += str(int(diff.days / 7)) + "W"
        elif abs(diff.days) > 0:
            output += str(diff.days) + "d"
        elif abs(diff.seconds) > 3600:
            output += str(int(diff.seconds / 3600)) + "h"
        elif abs(diff.seconds) > 60:
            output += str(int(diff.seconds / 60)) + "m"
        elif abs(diff.seconds) > 0:
            output += str(diff.seconds) + "s"
        else:
            output += "NOW"
        return output

    def print_date_entry(self, fmt=None):
        if fmt is None:
            return self.entry_date.strftime("%d-%m-%y %H:%M:%S")
        elif fmt == "abbr":
            return self.print_date_abbr(self.entry_date, datetime.now())
        elif fmt == "date":
            return self.entry_date.strftime("%d-%m-%y")
        elif fmt == "time":
            return self.entry_date.strftime("%H:%M:%S")
        else:
            return self.entry_date.strftime(fmt)

    def print_date_due(self, fmt=None):
        if fmt is None:
            return self.due_date.strftime("%d-%m-%y %H:%M:%S")
        elif fmt == "abbr":
            return self.print_date_abbr(datetime.now(), self.due_date)
        elif fmt == "date":
            return self.due_date.strftime("%d-%m-%y")
        elif fmt == "time":
            return self.due_date.strftime("%H:%M:%S")
        else:
            return self.due_date.strftime(fmt)

    def print_date_done(self, fmt=None):
        if fmt is None:
            return self.done_date.strftime("%d-%m-%y %H:%M:%S")
        elif fmt == "abbr":
            return self.print_date_abbr(self.done_date, datetime.now())
        elif fmt == "date":
            return self.done_date.strftime("%d-%m-%y")
        elif fmt == "time":
            return self.done_date.strftime("%H:%M:%S")
        else:
            return self.done_date.strftime(fmt)

    def parse_json(self, json_obj):
        pass

    def is_overdue(self):
        if self.due_date == datetime(0, 0, 0):
            return False
        elif self.due_date < datetime.now():
            return True
        return False

    def due_today(self):
        if self.due_date.date() == datetime.today().date():
            return True
        return False
