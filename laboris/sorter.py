from enum import Enum


class SortMethod(Enum):
    URG = 1
    DESCRIPTION = 2
    DUE = 3
    ENTRY = 4
    DONE = 5
    ID = 6
    UUID = 7
    PROJECT = 8
    TAG = 9
    STATUS = 10
    TIMES = 11
    PRIORITY = 12

    @staticmethod
    def get_method(method_str):
        rev = False
        if method_str[0] == '-':
            method_str = method_str[1:]
            rev = True
        hash_map = {
            "urg": SortMethod.URG,
            "urgency": SortMethod.URG,
            "description": SortMethod.DESCRIPTION,
            "due": SortMethod.DUE,
            "entry": SortMethod.ENTRY,
            "done": SortMethod.DONE,
            "id": SortMethod.ID,
            "uuid": SortMethod.UUID,
            "project": SortMethod.PROJECT,
            "tag": SortMethod.TAG,
            "status": SortMethod.STATUS,
            "times": SortMethod.TIMES,
            "priority": SortMethod.PRIORITY
        }
        if type(method_str) is not str:
            return SortMethod.URG, rev
        elif method_str in hash_map.keys():
            return hash_map[method_str], rev
        else:
            return SortMethod.URG, rev


def sort_task_set(task_set, method=SortMethod.URG, rev=False):
    if type(method) is str:
        method, rev = SortMethod.get_method(method)
    if method is SortMethod.URG:
        task_set.sort(key=lambda task: task.urgency, reverse=not (True is rev))
    elif method is SortMethod.DESCRIPTION:
        task_set.sort(
            key=lambda task: task.description, reverse=not (False is rev))
    elif method is SortMethod.DUE:
        task_set.sort(
            key=lambda task: str(task.due_date), reverse=not (False is rev))
    elif method is SortMethod.ENTRY:
        task_set.sort(
            key=lambda task: task.entry_date, reverse=not (False is rev))
    elif method is SortMethod.DONE:
        task_set.sort(
            key=lambda task: str(task.done_date), reverse=not (True is rev))
    elif method is SortMethod.ID:
        task_set.sort(
            key=lambda task: task.print_id(), reverse=not (True is rev))
    elif method is SortMethod.UUID:
        task_set.sort(
            key=lambda task: task.print_uuid(), reverse=not (True is rev))
    elif method is SortMethod.PROJECT:
        task_set.sort(
            key=lambda task: task.print_project(), reverse=not (True is rev))
    elif method is SortMethod.TAG:
        task_set.sort(
            key=lambda task: task.print_tag(), reverse=not (True is rev))
    elif method is SortMethod.STATUS:
        task_set.sort(
            key=lambda task: task.print_status(), reverse=not (True is rev))
    elif method is SortMethod.TIMES:
        task_set.sort(
            key=lambda task: task.total_time(), reverse=not (True is rev))
    elif method is SortMethod.PRIORITY:
        task_set.sort(key=lambda task: task.priority, reverse=not (True is rev))
