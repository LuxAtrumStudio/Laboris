"""
Laboris task manager task object
"""

from enum import Enum
from math import floor
import uuid
import datetime


class Task(object):
    """Laboris task object"""

    class Status(Enum):
        """Current status of the task object"""
        NONE = 0
        PENDING = 1
        DONE = 2

    def __init__(self, body=None):
        self.title = str()
        self.project = list()
        self.tag = list()
        self.uuid = None
        self.priority = int()
        self.modified_date = None
        self.entry_date = None
        self.due_date = None
        self.done_date = None
        self.status = self.Status.NONE
        self.times = list()
        self.urgency = float()  # TODO Calculate on server or client?
        self.is_active = False
        if body is not None:
            self.deserialize(body)

### Server Backup Work ###

    def create(self,
               title=str(),
               project=list(),
               tag=list(),
               priority=int(),
               due_date=None):
        """Creates a new task"""
        self.title = title
        self.project = project
        self.tag = tag
        self.priority = priority
        if due_date is None:
            self.due_date = None
        elif isinstance(due_date, datetime.datetime):
            self.due_date = due_date
        else:
            self.due_date = datetime.datetime.fromtimestamp(due_date)
        self.entry_date = datetime.datetime.now()
        self.status = self.Status.PENDING
        self.modified_date = datetime.datetime.now()
        self.calc_urgency()
        self.uuid = uuid.uuid1()

    def modify(self,
               title=None,
               project=None,
               tag=None,
               priority=None,
               due_date=None):
        """Modifies the task"""
        if title is not None:
            self.title = title
        if project is not None:
            self.project = project
        if tag is not None:
            self.tag = tag
        if priority is not None:
            self.priority = priority
        if due_date is not None:
            if isinstance(due_date, datetime.datetime):
                self.due_date = due_date
            else:
                self.due_date = datetime.datetime.fromtimestamp(due_date)
        self.modified_date = datetime.datetime.now()
        self.calc_urgency()

    def start(self, time=None):
        """Starts the timer for the task"""
        if self.is_active:
            return False
        if time is not None:
            if isinstance(time, datetime.datetime):
                self.times.append([time, None])
            else:
                self.times.append(
                    [datetime.datetime.fromtimestamp(time), None])
        else:
            self.times.append([datetime.datetime.now(), None])
        self.modified_date = datetime.datetime.now()
        return True

    def end(self, time=None):
        """Stops the timer for the task"""
        if not self.is_active:
            return False
        if time is not None:
            if isinstance(time, datetime.datetime):
                self.times[-1][1] = time
            else:
                self.times[-1][1] = datetime.datetime.fromtimestamp(time)
        else:
            self.times[-1][1] = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return True


### Client Side Work ###

    def get_color_key(self):
        """Gets the appropriate color for the task"""
        if self.is_active:
            return 'task.active'
        elif self.status == self.Status.DONE:
            return 'task.done'
        elif self.is_overdue():
            return 'task.overdue'
        elif self.is_due_today():
            return 'task.due_today'
        else:
            urgency_floor = floor(self.urgency)
            return 'task.urgency_{}'.format(urgency_floor)

    def is_overdue(self):
        """Checks if task is overdue"""
        if self.due_date is None:
            return False
        elif self.due_date < datetime.datetime.now():
            return True
        return False

    def is_due_today(self):
        """Checks if task is due today"""
        if self.due_date is None:
            return False
        elif self.due_date.date() == datetime.datetime.now().date():
            return True
        return False

    def check_is_active(self):
        """Checks if the task is currently active"""
        if self.times is not None and self.times[-1]['end'] is None:
            self.is_active = True
        else:
            self.is_active = False

    def calc_urgency(self):
        """Calculates the urgency of the task"""
        urg = 0.0
        urg += abs(2.00 * self.urgency_age())
        urg += abs(12.0 * self.urgency_due())
        urg += abs(0.20 * len(self.tag))
        urg += abs(1.00 * len(self.project))
        if self.is_active:
            urg += abs(1.0 * 4.0)
        if self.priority != -1:
            urg += abs(1.0 * self.priority)
        else:
            urg = 0.0
        if self.status == self.Status.DONE:
            urg = 0.0
        self.urgency = urg

    def urgency_age(self):
        """Finds urgency from the age, which is the number of days task has existed for divided by 400"""
        diff = datetime.datetime.now() - self.entry_date
        age = diff.days + (diff.seconds / 86400)
        return age / 400

    def urgency_due(self):
        """Finds the urgency from the due date"""
        if self.due_date is None:
            return 0.0
        if datetime.datetime.now() > self.due_date:
            diff = datetime.datetime.now() - self.due_date
            late = True
        else:
            diff = self.due_date - datetime.datetime.now()
            late = False
        overdue = diff.days + (diff.seconds / 86400)
        if not late:
            overdue *= -1
        if overdue > 7:
            return 1.0
        elif overdue >= -14:
            return float((overdue + 14) * 0.8 / 21) + 0.2
        return 0.2

    def deserialize(self, obj):
        """Reads json data to parse create the task object"""
        if 'tile' in obj:
            self.title = obj['title']
        if 'project' in obj:
            self.project = obj['project']
        if 'tag' in obj:
            self.tag = obj['tag']
        if 'uuid' in obj:
            self.uuid = obj['uuid']
        if 'priority' in obj:
            self.priority = obj['priority']
        if 'modifiedDate' in obj:
            self.modified_date = datetime.datetime.fromtimestamp(
                obj['modifiedDate'])
        if 'entryDate' in obj:
            self.entry_date = datetime.datetime.fromtimestamp(obj['entryDate'])
        if 'doneDate' in obj:
            self.done_date = datetime.datetime.fromtimestamp(obj['done_date'])
        if 'dueDate' in obj:
            self.due_date = datetime.datetime.fromtimestamp(obj['due_date'])
        if 'status' in obj:
            self.status = obj['status']
        if 'times' in obj:
            self.times = [[
                datetime.datetime.fromtimestamp(x[0]),
                datetime.datetime.fromtimestamp(x[1])
            ] for x in obj['times']]

    def serialize(self):
        """Writes the task object to a json data object"""
        return {
            'title':
            self.title,
            'project':
            self.project,
            'tag':
            self.tag,
            'uuid':
            self.uuid,
            'priority':
            self.priority,
            'modifiedDate':
            self.modified_date.timestamp()
            if self.modified_date else datetime.datetime.now(),
            'entryDate':
            self.entry_date.timestamp()
            if self.entry_date else datetime.datetime.now(),
            'dueDate':
            self.due_date.timestamp() if self.due_date else None,
            'doneDate':
            self.done_date.timestamp() if self.done_date else None,
            'status':
            self.status,
            'times': [[x[0].timestamp(), x[1].timestamp()] for x in self.times]
        }
