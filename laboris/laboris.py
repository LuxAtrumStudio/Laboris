from laboris.args import parse_args
import laboris.config as cfg
import laboris.data as dat
import laboris.reports.list
import laboris.reports.detail

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
        dat.sync(True, True if 'all' in args else False, True if 'completed' in args else False)
    elif args['action'] == 'report':
        if args['report'] == 'list':
            print(args)
            laboris.reports.list.main(args)
    elif 'task' in args:
        # TODO: Check that the task exists, othersize list, possible search list?
        laboris.reports.detail.main(args)
    else:
        laboris.reports.list.main(args)
