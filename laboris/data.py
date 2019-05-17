import json
import datetime
import os
import requests
import laboris.config as cfg

from math import exp


def datediff(a, b):
    diff = a - b
    return diff.days + (diff.seconds / 86400)


def urgdue(task):
    if task['dueDate'] is None:
        return 0.0
    due = datediff(datetime.datetime.now(),
                   datetime.datetime.fromtimestamp(task['dueDate']))
    k = 0.7
    x0 = -3.98677299562
    alpha = -5.966
    if due < alpha:
        return 0.2
    else:
        return 1.0 / (1 + exp(-k * (due - x0)))


def calc_urg(task):
    urg = 0.0
    urg += abs(0.01429 * datediff(
        datetime.datetime.fromtimestamp(task['entryDate']),
        datetime.datetime.now()))
    urg += abs(9.00000 * urgdue(task))
    urg += abs(1.00000 * len(task['projects']))
    urg += abs(0.20000 * len(task['tags']))
    urg += abs(1.00000 * task['priority'])
    urg += abs(4.0 if task['times'] and len(task['times'][-1]) == 1 else 0.0)
    if task['status'] == 'COMPLETED' or task['priority'] == -1:
        urg = 0.0
    return urg


def sync():
    global DATA
    if datetime.datetime.now().timestamp(
    ) > cfg.CONFIG['synced'] + cfg.CONFIG['syncTime']:
        cfg.note("Syncing to \"{}\"".format(cfg.CONFIG['url']))
        cfg.save_config()
        raw = requests.post(
            url=cfg.CONFIG['url'] + "sync",
            data={
                "datetime": int(cfg.CONFIG['synced'])
            }).json()
        for x in raw:
            ind = find_uuid(x['uuid'])
            if not ind:
                pass
            elif ind[0] >= 0:
                del DATA[0][ind[0]]
            elif ind[0] < 0:
                del DATA[1][-ind[0] + 1]
            if x['status'] == 'PENDING':
                DATA[0].append(x)
            else:
                DATA[1].append(x)
        cfg.CONFIG['synced'] = int(datetime.datetime.now().timestamp())
        cfg.save_config()
        save_data()


def update(id):
    if id >= 0:
        requests.post(
            url=cfg.CONFIG['url'] + "update/{}".format(DATA[0][id]['uuid']),
            dat=DATA[0][id])
    else:
        requests.post(
            url=cfg.CONFIG['url'] +
            "update/{}".format(DATA[1][-id + 1]['uuid']),
            dat=DATA[1][-id + 1])


def load_data():
    global DATA
    DATA = [[], []]
    if not os.path.exists(os.path.expanduser('~/.config/laboris/pending.json')):
        json.dump([],
                  open(
                      os.path.expanduser('~/.config/laboris/pending.json'),
                      'w'))
    if not os.path.exists(
            os.path.expanduser('~/.config/laboris/completed.json')):
        json.dump([],
                  open(
                      os.path.expanduser('~/.config/laboris/completed.json'),
                      'w'))
    DATA[0] = json.load(
        open(os.path.expanduser('~/.config/laboris/pending.json'), 'r'))
    DATA[1] = json.load(
        open(os.path.expanduser('~/.config/laboris/completed.json'), 'r'))
    sync()
    DATA[0] = sorted(
        [{
            "urg": calc_urg(x),
            **x
        } for x in DATA[0]],
        key=lambda x: x['urg'],
        reverse=True)


def save_data():
    json.dump(DATA[0],
              open(os.path.expanduser('~/.config/laboris/pending.json'), 'w'))
    json.dump(DATA[1],
              open(os.path.expanduser('~/.config/laboris/completed.json'), 'w'))


def find_uuid(uuid, pending=None):
    if pending is None:
        entries = DATA[0]
    else:
        entries = DATA[0] if pending else DATA[1]
    matches = []
    for i, ent in enumerate(entries):
        if ent['uuid'] == uuid or ent['uuid'].startswith(uuid):
            matches.append(i)
    if pending is None:
        for i, ent in enumerate(DATA[1]):
            if ent['uuid'] == uuid or ent['uuid'].startswith(uuid):
                matches.append(-i - 1)
    return matches


def create(args):
    entry = {
        "title": args.title,
        "projects": args.project,
        "tags": args.tag,
        "priority": args.pri,
        "dueDate": args.due.timestamp() if args.due else None
    }
    raw = requests.post(url=cfg.CONFIG['url'], data=entry).json()
    DATA[0].append(raw['entry'])


def modify(args):
    entry = {
        "title": args.title,
        "projects": args.project,
        "tags": args.tag,
        "priority": args.pri,
        "dueDate": args.due.timestamp() if args.due else None
    }
    raw = requests.post(url=cfg.CONFIG['url'], data=entry).json()
    DATA[0].append(raw['entry'])
