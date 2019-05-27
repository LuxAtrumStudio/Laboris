from laboris.args import parse_args
import laboris.config as cfg
import laboris.data as dat
from laboris.reports.list import status, detail

def main():
    args = parse_args()
    cfg.load_config()
    dat.load_data()
    if args.action == 'add':
        dat.create(args)
        dat.save_data()
    elif args.task != None:
        detail(args)
    else:
        status(args)
