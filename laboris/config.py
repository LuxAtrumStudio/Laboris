import json
import os
import math


def gen_config():
    global CONFIG
    if not os.path.exists(os.path.expanduser('~/.config/laboris')):
        os.makedirs(os.path.expanduser('~/.config/laboris'))
    CONFIG = {
        "synced": 0,
        "syncTime": 600,
        "autoSync": True,
        "url": input("\033[35;1mServer URL\033[0m: "),
        "theme": {
            "bg": "\033[40m",
            "title": "\033[97;1;4m",
            "project": "\033[36m",
            "tag": "\033[33m",
            "msgSuccess": "\033[32;1m",
            "msgNote": "\033[36;1m",
            "msgWarning": "\033[33;1m",
            "msgError": "\033[31;1m",
            "actAdd": "\033[34;1m",
            "actModify": "\033[35;1m",
            "actComplete": "\033[32;1m",
            "actDelete": "\033[31;1m",
            "actStart": "\033[33;1m",
            "actStop": "\033[33;1m",
            "staActive": "\033[30;42m",
            "staOverdue": "\033[30;1;4;41m",
            "staDueToday": "\033[31;1;43m",
            "urgency": {
                "0-3": ["\033[39m"],
                "3-6": ["#2196f3", "#6caf50"],
                "6-8": ["#6caf50", "#FFEB3B"],
                "8-9": ["#ffeb3b", "#f44336"],
                "9-10": ["#f44336", "bold"],
                "10+": ["#f44336", "bold", "underline"]
            }
        }
    }
    json.dump(CONFIG,
              open(os.path.expanduser('~/.config/laboris/config.json'), 'w'))


def load_config():
    global CONFIG
    CONFIG = {}
    if os.path.isfile(os.path.expanduser('~/.config/laboris/config.json')):
        CONFIG = json.load(
            open(os.path.expanduser('~/.config/laboris/config.json'), 'r'))
    else:
        gen_config()


def save_config():
    if os.path.isfile(os.path.expanduser('~/.config/laboris/config.json')):
        json.dump(CONFIG,
                  open(
                      os.path.expanduser('~/.config/laboris/config.json'), 'w'))


def note(msg):
    print("{}{}\033[0m".format(CONFIG['theme']['msgNote'], msg))


def get_urg(urg):
    res = ""
    a , b, col = None, None, None
    for key in CONFIG['theme']['urgency']:
        if '-' in key:
            start, end = map(float, key.split('-'))
        elif key[-1] == '+':
            start = float(key[:-1])
            end = math.inf
        if start <= urg < end:
            if len(CONFIG['theme']['urgency'][key]) == 1:
                if CONFIG['theme']['urgency'][key][0][0] == '#':
                    a = tuple(
                            int(CONFIG['theme']['urgency'][key][0][1:][i:i + 2], 16)
                        for i in (0, 2, 4))
                else:
                    res = CONFIG['theme']['urgency'][key][0]
            else:
                if CONFIG['theme']['urgency'][key][0][0] == '#':
                    a = tuple(
                            int(CONFIG['theme']['urgency'][key][0][1:][i:i + 2], 16)
                        for i in (0, 2, 4))
                if CONFIG['theme']['urgency'][key][1][0] == '#':
                    b = tuple(
                            int(CONFIG['theme']['urgency'][key][1][1:][i:i + 2], 16)
                        for i in (0, 2, 4))
            if a and b:
                urg = urg -  float(key.split('-')[0])
                dt = (b[0] - a[0], b[1]-a[1], b[2] - a[2])
                col = (a[0] + dt[0]*urg, a[1] + dt[1]*urg, a[2] + dt[2]*urg)
            if col:
                res = "\033[38;2;{};{};{}m".format(int(col[0]), int(col[1]), int(col[2]))
    return res

