from laboris.args import parse_args
import laboris.config as cfg
import laboris.data as dat
from laboris.reports.list import status, detail

def main():
    args = parse_args()
    cfg.load_config()
    dat.load_data()
    if args['action']== 'add':
        dat.create(args)
        dat.save_data()
    elif args['action'] == 'modify':
        dat.modify(args)
        dat.save_data()
    elif args['action'] == 'start':
        dat.start(args)
        dat.save_data()
    elif args['action'] == 'stop':
        dat.stop(args)
        dat.save_data()
    elif args['action'] == 'done':
        dat.done(args)
        dat.save_data()
    elif args['action'] == 'undone':
        dat.undone(args)
        dat.save_data()
    elif args['action'] == 'delete':
        dat.delete(args)
        dat.save_data()
    elif args['action'] == 'sync':
        print(args)
        dat.sync(True, True if 'all' in args else False)
    elif 'task' in args:
        detail(args)
    else:
        status(args)
