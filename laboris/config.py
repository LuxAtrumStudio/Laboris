import json
import os


def gen_config():
    global CONFIG
    if not os.path.exists(os.path.expanduser('~/.config/laboris')):
        os.makedirs(os.path.expanduser('~/.config/laboris'))
    CONFIG = {
        "synced": 0,
        "syncTime": 60,
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
                "0-3": "\033[39m",
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
    for key in CONFIG['theme']['urgency']:
        if '-' in key:
            start, end = map(float, key.split('-'))
        elif key[-1] == '+':
            start = float(key[:-1])
            end = inf
        if start <= urg < end:
            if len(CONFIG['theme']['urgency'][key]) == 1:
                a = tuple(
                    int(CONFIG['theme']['urgency'][key][0][i:i + 2], 16)
                    for i in (0, 2, 4))
            else:
                a = tuple(
                    int(CONFIG['theme']['urgency'][key][0][i:i + 2], 16)
                    for i in (0, 2, 4))
                b = tuple(
                    int(CONFIG['theme']['urgency'][key][1][i:i + 2], 16)
                    for i in (0, 2, 4))

