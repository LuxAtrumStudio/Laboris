import json
import datetime
import os
import sys
import requests
import uuid
import laboris.config as cfg
from laboris.fuzz import weighted_fuzz
from laboris.prompt import select, yn_choice

from math import exp, log

def datediff(a, b):
    diff = a - b
    return diff.days + (diff.seconds / 86400)


def urgdue(task):
    if 'dueDate' not in task or task['dueDate'] is None:
        return 0.0
    due = datediff(datetime.datetime.now(),
                   datetime.datetime.fromtimestamp(task['dueDate']))
    age = datediff(datetime.datetime.fromtimestamp(task['entryDate']), datetime.datetime.fromtimestamp(task['dueDate']))
    k = log(81)/age
    x0 = log(1/9) / -k
    return 1.0 / (1 + exp(-k * (due + x0)))


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

def post(url, data=None, required=False):
    try:
        res = requests.post(url=url, data=data)
        return res.json()
    except:
        if required is False:
            return []
        else:
            print("Failed to post to \"{}\"".format(url))
            sys.exit(3)


def sync(force=False, historical=False, completed=False):
    global DATA
    if 'synced' not in cfg.CONFIG or datetime.datetime.now().timestamp() > cfg.CONFIG['synced'] + cfg.CONFIG['syncTime'] or force:
        cfg.note("Syncing to \"{}\"".format(cfg.CONFIG['url']))
        cfg.save_config()
        if historical is True:
            cfg.CONFIG['synced'] = 0
        updated_data = [{i:d[i] for i in d if i not in ('urg')} for d in DATA[0] if d['modifiedDate'] > cfg.CONFIG['synced']]
        if completed:
            updated_data += [{i:d[i] for i in d if i not in ('urg')} for d in DATA[1] if d['modifiedDate'] > cfg.CONFIG['synced']]
        raw = []
        if len(updated_data) >= 20:
            for i in range(0, len(updated_data), 20):
                raw += post(
                    url=cfg.CONFIG['url'] + "/sync",
                    data={
                        "datetime": int(cfg.CONFIG['synced']),
                        "entries": json.dumps(updated_data[i:i+20])
                    }, required=True)
        else:
            raw = post(
                url=cfg.CONFIG['url'] + "/sync",
                data={
                    "datetime": int(cfg.CONFIG['synced']),
                    "entries": json.dumps(updated_data)
                }, required=False)
        for x in raw:
            if x['modifiedDate'] < cfg.CONFIG['synced']:
                continue
            ind = find_uuid(x['uuid'])
            if not ind:
                pass
            elif ind[0] >= 0:
                del DATA[0][ind[0]]
            elif ind[0] < 0:
                del DATA[1][-ind[0] - 1]
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
            url=cfg.CONFIG['url'] + "/update/{}".format(DATA[0][id]['uuid']),
            dat=DATA[0][id])
    else:
        requests.post(
            url=cfg.CONFIG['url'] +
            "update/{}".format(DATA[1][-id - 1]['uuid']),
            dat=DATA[1][-id - 1])

def log_failed(url):
    with open("~/.config/laboris/requests.txt", "w+") as file:
        file.write(url + '\n')

def sync_failed():
    with open('~/.config/laboris/requests.txt', 'r') as file:
        requests = [x.strip() for x in file.readlines()]
    failed = []
    for request in requests:
        if post(request) == []:
            failed.append(request)
    with open('~/.config/laboris/requests.txt', 'w') as file:
        file.writelines(failed)


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
            "id": i,
            **x
        } for i, x in enumerate(DATA[0])],
        key=lambda x: x['urg'],
        reverse=True)


def save_data():
    DATA[0] = [{i:d[i] for i in d if i not in ('urg', 'id')} for d in DATA[0]]
    DATA[0] = sorted(DATA[0], key=lambda x: x['entryDate'])
    DATA[1] = sorted(DATA[1], key=lambda x: x['entryDate'])
    json.dump(DATA[0],
              open(os.path.expanduser('~/.config/laboris/pending.json'), 'w'))
    json.dump(DATA[1],
              open(os.path.expanduser('~/.config/laboris/completed.json'), 'w'))

def format_task(tsk):
    task_color = cfg.get_urg(calc_urg(tsk))
    if 'dueDate' in tsk and tsk['dueDate'] and datetime.datetime.fromtimestamp(tsk['dueDate']).date() == datetime.datetime.now().date():
        task_color = cfg.CONFIG['theme']['staDueToday']
    elif 'dueDate' in tsk and tsk['dueDate'] and datetime.datetime.fromtimestamp(tsk['dueDate']).date() < datetime.datetime.now().date():
        task_color = cfg.CONFIG['theme']['staOverdue']
    elif 'times' in tsk and tsk['times'] and len(tsk['times'][-1]) == 1:
        task_color = cfg.CONFIG['theme']['staActive']
    res = "{}{}\033[0m".format(task_color, tsk['title'])
    res += (" +" + " +".join(tsk['projects']) if tsk['projects'] else '')
    res += (" @" + " @".join(tsk['tags']) if tsk['tags'] else '')
    return res


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

def find(arg):
    matches = []
    if arg.isdigit():
        arg = int(arg)
        for i, ent in enumerate(DATA[0]):
            if ent['id'] == arg:
                return i
    else:
        for i, ent in enumerate(DATA[0]):
            if ent['uuid'] == arg or ent['uuid'].startswith(arg):
                matches.append(i)
            if ent['title'] == arg:
                return i
            elif ent['title'].lower().startswith(arg.lower()):
                matches.append(i)
        if len(matches) > 1:
            data = sorted([[i, calc_urg(DATA[0][i])] for i in matches], key=lambda x: x[1], reverse=True)
            selected = select("Specify Task:", [format_task(DATA[0][v[0]]) for v in data])
            matches = [data[selected][0]]
    if not matches:
        for i, ent in enumerate(DATA[1]):
            if ent['uuid'] == arg or ent['uuid'].startswith(arg):
                matches.append(-i-1)
            if ent['title'] == arg:
                return -i - 1
        if len(matches) > 1:
            data = sorted([[i, calc_urg(DATA[1][i])] for i in matches], key=lambda x: x[1], reverse=True)
            selected = select("Specify Task:", [format_task(DATA[1][v[0]]) for v in data])
            matches = [data[selected][0]]
    return matches[0]


def create(args):
    entry = {
        "title": args['title'],
        "projects": args['projects'],
        "tags": args['tags'],
        "priority": args['priority'],
        "dueDate": args['dueDate'].timestamp() if 'dueDate' in args else None,
        "status": 'PENDING',
        "entryDate": int(datetime.datetime.now().timestamp()),
        "modifiedDate": int(datetime.datetime.now().timestamp()),
        "times": [],
        "uuid": str(uuid.uuid3(uuid.NAMESPACE_URL, "{}{}".format(args['title'], datetime.datetime.now())))
    }
    DATA[0].append(entry)

    if cfg.CONFIG['autoSync']:
        post(url=cfg.CONFIG['url'], data=entry)


def modify(args):
    idx = find(args['uuid'])
    if idx >= 0:
        task = DATA[0][idx]
    else:
        task = DATA[1][-idx-1]
    if 'dueDate' in args:
        args['dueDate'] = int(args['dueDate'].timestamp())
    args['modifiedDate'] = int(datetime.datetime.now().timestamp())
    args = {i:args[i] for i in args if i not in ('urg', 'action', 'uuid')}
    for key in args.keys():
        task[key]=args[key]
    if idx >= 0:
        DATA[0][idx] = task
    else:
        DATA[1][-idx-1] = task
    if cfg.CONFIG['autoSync']:
        post(url=cfg.CONFIG['url'] + "/update/{}".format(task['uuid']), data=args)

def start(args):
    idx = find(args['uuid'])
    if idx >= 0:
        task = DATA[0][idx]
    else:
        task = DATA[1][-idx-1]
    if 'time' in args:
        task['times'].append([int(args['time'].timestamp())])
    else:
        task['times'].append([int(datetime.datetime.now().timestamp())])
    task['modifiedDate'] = int(datetime.datetime.now().timestamp())
    if cfg.CONFIG['autoSync']:
        post(url=cfg.CONFIG['url'] + "/update/{}".format(task['uuid']), data=json.dumps(task['times']))

def stop(args):
    idx = find(args['uuid'])
    if idx >= 0:
        task = DATA[0][idx]
    else:
        task = DATA[1][-idx-1]
    if 'time' in args:
        task['times'][-1].append(int(args['time'].timestamp()))
    else:
        task['times'][-1].append(int(datetime.datetime.now().timestamp()))
    task['modifiedDate'] = int(datetime.datetime.now().timestamp())
    if cfg.CONFIG['autoSync']:
        post(url=cfg.CONFIG['url'] + "/update/{}".format(task['uuid']), data=json.dumps(task['times']))

def done(args):
    idx = find(args['uuid'])
    if idx < 0:
        print("laboris done warning: Task {}[{}] is already done", DATA[1][-idx-1]['title'], args['uuid'])
    DATA[1].append(DATA[0][idx])
    DATA[1][-1]['status']='COMPLETED'
    DATA[1][-1]['modifiedDate'] = int(datetime.datetime.now().timestamp())
    del DATA[0][idx]
    if cfg.CONFIG['autoSync']:
        post(url=cfg.CONFIG['url'] + "/update/{}".format(DATA[1][-1]['uuid']), data={'status': 'COMPLETED'})

def undone(args):
    idx = find(args['uuid'])
    if idx >= 0:
        print("laboris undone warning: Task {}[{}] is already pending", DATA[0][idx]['title'], args['uuid'])
    DATA[0].append(DATA[1][-idx-1])
    DATA[0][-1]['status']='PENDING'
    DATA[0][-1]['modifiedDate'] = int(datetime.datetime.now().timestamp())
    del DATA[1][-idx-1]
    if cfg.CONFIG['autoSync']:
        post(url=cfg.CONFIG['url'] + "/update/{}".format(DATA[0][-1]['uuid']), data={'status': 'PENDING'})

def delete(args):
    idx = find(args['uuid'])
    if idx >= 0 and yn_choice("Delete: {}".format(format_task(DATA[0][idx]))):
        res = post(url=cfg.CONFIG['url'] + "/delete/{}".format(DATA[0][idx]['uuid']))
        if res == []:
            pass
        del DATA[0][idx]
    elif idx < 0 and yn_choice("Delete: {}".format(format_task(DATA[1][-idx-1]))):
        res = post(url=cfg.CONFIG['url'] + "/delete/{}".format(DATA[1][-idx-1]['uuid']))
        if res == []:
            pass
        del DATA[1][-idx-1]
