import json
import task
import os


def load_data():
    path_pending = os.path.expanduser("~/.laboris/pending.json")
    path_done = os.path.expanduser("~/.laboris/done.json")
    with open(path_pending) as data:
        pending_data = json.load(data)
    with open(path_done) as data:
        done_data = json.load(data)

    pending_tasks = []
    done_tasks = []
    for entry in pending_data:
        new_task = task.Task()
        new_task.parse_json(entry)
        new_task.id = len(pending_tasks) + 1
        pending_tasks.append(new_task)
    for entry in done_data:
        new_task = task.Task()
        new_task.status = new_task.Status.DONE
        new_task.parse_json(entry)
        new_task.id = len(done_tasks) + 1
        done_tasks.append(new_task)

    return pending_tasks, done_tasks


def save_data(pending_tasks, done_tasks):
    pending_tasks = sorted(pending_tasks, key=lambda task: task.entry_date)
    done_tasks = sorted(done_tasks, key=lambda task: task.entry_date)
    path_pending = os.path.expanduser("~/.laboris/pending.json")
    pending_data = []
    for t in pending_tasks:
        pending_data.append(t.get_json())
    path_done = os.path.expanduser("~/.laboris/done.json")
    done_data = []
    for t in done_tasks:
        done_data.append(t.get_json())
    with open(path_pending, "w") as data:
        json.dump(pending_data, data)
    with open(path_done, "w") as data:
        json.dump(done_data, data)

