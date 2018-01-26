import os
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
    data = json.load(open(os.path.expanduser("~/.laboris/default.json")))
    theme.parse_json(data["theme"])
    pending, done = laboris.data.load_data()


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
