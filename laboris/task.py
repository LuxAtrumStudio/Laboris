"""This is the task module that contains task and time data"""

import time
import laboris.interval as interval
import json
import uuid
from enum import Enum
from datetime import datetime, date, time


class Task:

    class Status(Enum):
        DONE = 1
        PENDING = 2

    def __init__(self,
                 _desc=str(),
                 _project=list(),
                 _tag=list(),
                 _priority=int(),
                 _entry=None,
                 _due=None,
                 _done=None):
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
        self.id = int()
        self.times = list()
        self.active = False
        self.set_urg = False

    def print_project(self, index=None):
        if index == "size":
            m = 0
            for p in self.project:
                m = max(m, len(p))
            return " " * m
        if type(index) is str:
            index = int(index)
        if index is None:
            output = str()
            for p in self.project:
                output += p + " "
            return output[:-1]
        if len(self.project) > index:
            return self.project[index]
        else:
            return str()

    def print_tag(self, index=None):
        if index == "size":
            m = 0
            for t in self.tag:
                m = max(m, len(t))
            return " " * m
        if type(index) is str:
            index = int(index)
        if index is None:
            output = str()
            for t in self.tag:
                output += t + " "
            return output[:-1]
        if len(self.tag) > index:
            return self.tag[index]
        else:
            return str()

    def print_id(self):
        if self.status is self.Status.DONE:
            return "-"
        else:
            return str(self.id)

    def print_uuid(self, fmt=None):
        if fmt is None or fmt == "long":
            return str(self.uuid)
        elif fmt == "short":
            return str(self.uuid)[:8]
        else:
            return ""

    def print_status(self, fmt=None):
        if self.active is True:
            if fmt is None or fmt == "short":
                return "A"
            elif fmt is "long":
                return "Active"
            else:
                return ""
        if self.status is self.Status.PENDING:
            if fmt is None or fmt == "short":
                return "P"
            elif fmt == "long":
                return "Pending"
            else:
                return ""
        elif self.status is self.Status.DONE:
            if fmt is None or fmt == "short":
                return "C"
            elif fmt == "long":
                return "Completed"
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
            return self.entry_date.strftime("%d-%m-%Y %H:%M:%S")
        elif fmt == "abbr":
            return self.print_date_abbr(self.entry_date, datetime.now())
        elif fmt == "date":
            return self.entry_date.strftime("%d-%m-%Y")
        elif fmt == "time":
            return self.entry_date.strftime("%H:%M:%S")
        else:
            return self.entry_date.strftime(fmt)

    def print_date_due(self, fmt=None):
        if self.due_date is None:
            return str()
        if fmt is None:
            return self.due_date.strftime("%d-%m-%Y %H:%M:%S")
        elif fmt == "abbr":
            return self.print_date_abbr(datetime.now(), self.due_date)
        elif fmt == "date":
            return self.due_date.strftime("%d-%m-%Y")
        elif fmt == "time":
            return self.due_date.strftime("%H:%M:%S")
        else:
            return self.due_date.strftime(fmt)

    def print_date_done(self, fmt=None):
        if self.done_date is None:
            return str()
        if fmt is None:
            return self.done_date.strftime("%d-%m-%Y %H:%M:%S")
        elif fmt == "abbr":
            return self.print_date_abbr(self.done_date, datetime.now())
        elif fmt == "date":
            return self.done_date.strftime("%d-%m-%Y")
        elif fmt == "time":
            return self.done_date.strftime("%H:%M:%S")
        else:
            return self.done_date.strftime(fmt)

    def print_interval(self, fmt=None, sec=False, index=None):
        if type(fmt) is str and fmt.isdigit():
            index = int(fmt)
            fmt = None
        if fmt is None or fmt == str():
            fmt = "all"
        if fmt == "total":
            sec = 0
            for t in self.times:
                sec += t.get_duration()
            minute = int(sec / 60)
            sec -= minute * 60
            hour = int(minute / 60)
            minute -= hour * 60
            return "{0:02}:{1:02}".format(hour, minute)
        if index is None:
            output = str()
            for t in self.times:
                if fmt == "start":
                    output += t.print_start(sec) + "\n"
                elif fmt == "end":
                    output += t.print_end(sec) + "\n"
                elif fmt == "duration":
                    output += t.print_duration(sec) + "\n"
                elif fmt == "all":
                    output += t.print_start(sec) + " - " + t.print_end(
                        sec) + ": " + t.print_duration(sec) + "\n"
            return output[:-1]
        elif len(self.times) > index:
            if fmt == "start":
                return self.times[index].print_start(sec)
            elif fmt == "end":
                return self.times[index].print_end(sec)
            elif fmt == "duration":
                return self.times[index].print_duration(sec)
            elif fmt == "all":
                return self.times[index].print_start(sec) + " - " + self.times[index].print_end(sec) + ": " +\
                        self.times[index].print_duration(sec)
        return ""

    def print_fmt(self, fmt, sizes=None):
        fmt = fmt.split('|')
        output = str()
        if sizes is None:
            sizes = [0] * len(fmt)
        for i, entry in enumerate(fmt):
            add = entry.split(';')
            if len(add) > 1:
                add = add[1]
            else:
                add = None
            if entry == "description":
                output += "{:<{}}".format(self.description, sizes[i])
            elif entry.startswith("project"):
                output += "{:<{}}".format(self.print_project(add), sizes[i])
            elif entry.startswith("tag"):
                output += "{:<{}}".format(self.print_tag(add), sizes[i])
            elif entry == "priority" or entry == 'p':
                output += "{:<{}}".format(self.priority, sizes[i])
            elif entry == "urgency" or entry == "urg":
                output += "{:<{}}".format("{:.3}".format(self.urgency),
                                          sizes[i])
            elif entry == "id":
                output += "{:>{}}".format(self.print_id(), sizes[i])
            elif entry.startswith("times"):
                output += "{:<{}}".format(self.print_interval(add), sizes[i])
            elif entry.startswith("uuid"):
                output += "{:<{}}".format(self.print_uuid(add), sizes[i])
            elif entry.startswith("entry") or entry.startswith("age"):
                output += "{:>{}}".format(self.print_date_entry(add), sizes[i])
            elif entry.startswith("due"):
                output += "{:>{}}".format(self.print_date_due(add), sizes[i])
            elif entry.startswith("done"):
                output += "{:>{}}".format(self.print_date_done(add), sizes[i])
            elif entry.startswith("status") or entry.startswith("st"):
                output += "{:<{}}".format(self.print_status(add), sizes[i])
            output += ' '
        output = output[:-1]
        return output

    def task_color(self, txt):
        import laboris.settings as s
        if self.active is True:
            txt = s._theme.get_color("active") + txt + s._theme.reset()
        elif self.status == self.Status.DONE:
            txt = s._theme.get_color("done") + txt + s._theme.reset()
        elif self.is_overdue() is True:
            txt = s._theme.get_color("overdue") + txt + s._theme.reset()
        elif self.due_today() is True:
            txt = s._theme.get_color("due_today") + txt + s._theme.reset()
        elif self.urgency > 10:
            txt = s._theme.get_color("urg10") + txt + s._theme.reset()
        elif self.urgency > 9:
            txt = s._theme.get_color("urg9") + txt + s._theme.reset()
        elif self.urgency > 8:
            txt = s._theme.get_color("urg8") + txt + s._theme.reset()
        elif self.urgency > 7:
            txt = s._theme.get_color("urg7") + txt + s._theme.reset()
        elif self.urgency > 6:
            txt = s._theme.get_color("urg6") + txt + s._theme.reset()
        elif self.urgency > 5:
            txt = s._theme.get_color("urg5") + txt + s._theme.reset()
        elif self.urgency > 4:
            txt = s._theme.get_color("urg4") + txt + s._theme.reset()
        elif self.urgency > 3:
            txt = s._theme.get_color("urg3") + txt + s._theme.reset()
        elif self.urgency > 2:
            txt = s._theme.get_color("urg2") + txt + s._theme.reset()
        elif self.urgency > 1:
            txt = s._theme.get_color("urg1") + txt + s._theme.reset()
        return txt

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
        if 'times' in json_obj:
            for t in json_obj['times']:
                new_interval = interval.Interval()
                new_interval.parse_json(t)
                self.times.append(new_interval)
                if new_interval.is_done() is False:
                    self.active = True
        if "urg" in json_obj.keys():
            self.urgency = json_obj["urg"]
            self.set_urg = True
        else:
            self.calculate_urgency()
        self.uuid = uuid.uuid3(
            uuid.NAMESPACE_URL,
            self.description + self.entry_date.strftime("%Y%m%d%H%M%S"))

    def get_json(self):
        data = dict()
        data['description'] = self.description
        data['priority'] = self.priority
        data['project'] = self.project
        data['tag'] = self.tag
        data['entry'] = int(self.entry_date.timestamp())
        if self.set_urg is True:
            data['urg'] = self.urgency
        if self.due_date is not None:
            data['due'] = int(self.due_date.timestamp())
        if self.done_date is not None:
            data['done'] = int(self.done_date.timestamp())
        if len(self.times) != 0:
            data['times'] = list()
            for t in self.times:
                data['times'].append(t.get_json())
        return data

    def get_age(self):
        if self.done_date is None:
            age = datetime.now() - self.entry_date
        else:
            age = self.done_date - self.entry_date
        return int(age.seconds)

    def total_time(self):
        total = 0
        for t in self.times:
            total += t.duration()
        return total

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
        if self.active is True:
            self.urgency += abs(1.0 * 4)
        if self.status is self.Status.DONE:
            self.urgency = 0.0
        if self.urgency <= 0.009:
            self.urgency = 0.0

    def urgency_age(self):
        diff = datetime.now() - self.entry_date
        age = diff.days + (diff.seconds / 86400)
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
        overdue = diff.days + (diff.seconds / 86400)
        if late is False:
            overdue *= -1
        if overdue > 7:
            return 1.0
        elif overdue >= -14:
            return float((overdue + 14) * 0.8 / 21) + 0.2
        else:
            return 2.0
