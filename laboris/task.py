"""
Laboris task manager task object
"""

from enum import Enum
import datetime


class Task(object):
    class Status(Enum):
        NONE = 0
        PENDING = 1
        DONE = 2

    def __init__(self):
        self.title = str()
        self.project = list()
        self.tag = list()
        self.uuid = None
        self.priority = int()
        self.urgency = float()  # TODO Calculate on server or client?
        self.modified_date = None
        self.entry_date = None
        self.due_date = None
        self.done_date = None
        self.status = self.Status.NONE
        self.times = list()

    def deserialize(self, obj):
        if 'tile' in obj:
            self.title = obj['title']
        if 'project' in obj:
            self.project = obj['project']

    def serialize(self):
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
            'modified_date':
            self.modified_date.timestamp()
            if self.modified_date else datetime.datetime.now(),
            'entry_date':
            self.entry_date.timestamp()
            if self.entry_date else datetime.datetime.now(),
            'due_date':
            self.due_date.timestamp() if self.due_date else None,
            'done_date':
            self.done_date.timestamp() if self.done_date else None,
            'status':
            self.status,
            'times':
            self.times
        }
