import os
import sys
import json
import laboris.theme
import laboris.data

#  _theme = theme.Theme()
#  _pending = list()
#  _done = list()

theme = laboris.theme.Theme()
data = dict()
pending = list()
done = list()


def init():
    global theme
    global pending
    global done
    global data
    if os.path.exists(os.path.expanduser("~/.config/laboris")) is False:
        dne()
    data = json.load(open(os.path.expanduser(
        "~/.config/laboris/default.json")))
    theme.parse_json(data["theme"])
    pending, done = laboris.data.load_data()


def dne():
    yn = input("Laboris config/data files does not exist.\n"
               "Would you like to create them? [Y/n] ")
    if yn.lower() in ('y', 'yes'):
        os.makedirs(os.path.expanduser("~/.config/laboris"))
        with open(os.path.expanduser("~/.config/laboris/default.json"), 'w') as file:
            file.write('{"theme": {"background": 40, "title": [97, -1, 1, 4], "add": [33, -1], "completed": [32, -1], "delete": [31, -1], "start": [33, -1], "stop": [33, -1], "err": [31, -1, 1], "warn": [33, -1, 1], "overdue": [30, 41], "due_today": [31, 43], "urg10": [31, -1, 1], "urg9": [31, -1], "urg8": [31, -1], "urg7": [33, -1], "active": [30, 42], "reports.graph.active": [32, -1], "reports.burndown.pending": [-1, 41], "reports.burndown.started": [-1, 43], "reports.burndown.done": [-1, 42]}}')
        with open(os.path.expanduser("~/.config/laboris/pending.json"), 'w') as file:
            file.write("[]")
        with open(os.path.expanduser("~/.config/laboris/done.json"), 'w') as file:
            file.write("[]")
    sys.exit(0)


def term():
    global pending
    global done
    laboris.data.save_data(pending, done)


def str_ref(dic, path):
    if path.split('.')[0] not in dic.keys():
        return None
    else:
        key = path.split('.')[0]
        path = '.'.join(path.split('.')[1:])
        if path == str():
            return dic[key]
        else:
            return str_ref(dic[key], path)


def get_data(path):
    global data
    return str_ref(data, path)


def in_data(path):
    if get_data(path) is not None:
        return True
    return False
