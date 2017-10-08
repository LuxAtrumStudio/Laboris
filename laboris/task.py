"""This is the task module that contains task and time data"""

import time
import json
import itertools
import collections
import uuid
from enum import Enum
from datetime import datetime, date, time


class Task:
    class Status(Enum):
        DONE = 1
        PENDING = 2

    def __init__(self, _desc=str(), _project=list(), _tag=(), _priority=int(), _entry=None, _due=None, _done=None):
        self.description = _desc
        self.project = _project
        self.tag = _tag
        self.uuid = uuid.uuid1()
        self.priority = _priority
        self.urgency = float()
        self.entry_date = _entry
        self.due_date = _due
        self.done_date = _done
        self.status = self.Status.PENDING

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

    def print_status(self, fmt=None):
        if self.status is self.Status.PENDING:
            if fmt is None or fmt == "short":
                return "P"
            elif fmt == "long":
                return "Pending"
            else:
                return ""
        elif self.status is self.Status.DONE:
            if fmt is None or fmt == "short":
                return "D"
            elif fmt == "long":
                return "Done"
            else:
                return ""
        else:
            return ""


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
            output = "NOW"
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
        if self.due_date is None:
            return str()
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
        if self.done_date is None:
            return str()
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
        self.description = json_obj['description']
        self.priority = json_obj['priority']
        self.project = json_obj['project']
        self.tag = json_obj['tag']
        self.entry_date = datetime.fromtimestamp(json_obj['entry'])
        if 'due' in json_obj:
            self.due_date = datetime.fromtimestamp((json_obj['due']))
        else:
            self.due_date = None
        if 'done' in json_obj:
            self.done_date = datetime.fromtimestamp((json_obj['done']))
        else:
            self.done_date = None
        self.calculate_urgency()

    def get_json(self):
        data = dict()
        data['description'] = self.description
        data['priority'] = self.priority
        data['project'] = self.project
        data['tag'] = self.tag
        data['entry'] = self.entry_date.timestamp()
        if self.due_date is not None:
            data['due'] = self.due_date.timestamp()
        if self.done_date is not None:
            data['done'] = self.done_date.timestamp()
        return data

    def is_overdue(self):
        if self.due_date is None:
            return False
        elif self.due_date < datetime.now():
            return True
        return False

    def due_today(self):
        if self.due_date is None:
            return False
        if self.due_date.date() == datetime.today().date():
            return True
        return False

    def calculate_urgency(self):
        self.urgency = 0.0
        self.urgency += abs(2.00 * self.urgency_age())
        self.urgency += abs(12.0 * self.urgency_due())
        self.urgency += abs(1.00 * self.priority)
        self.urgency += abs(0.20 * len(self.tag))
        self.urgency += abs(1.00 * len(self.project))
        if self.status is self.Status.DONE:
            self.urgency = 0.0

    def urgency_age(self):
        diff = datetime.now() - self.entry_date
        age = diff.days + (diff.seconds * 86400)
        return age / 400

    def urgency_due(self):
        if self.due_date is None:
            return 0.0
        late = False
        if datetime.now() > self.due_date:
            diff = datetime.now() - self.due_date
            late = True
        else:
            diff = self.due_date - datetime.now()
        print("DAY: {}  SEC: {}".format(diff.days, diff.seconds))
        overdue = diff.days + (diff.seconds / 86400)
        print("OVERDUE: {}".format(overdue))
        if late is False:
            overdue *= -1
        if overdue > 7:
            return 1.0
        elif overdue >= -14:
            return float((overdue + 14) * 0.8 / 21) + 0.2
        else:
            return 2.0
