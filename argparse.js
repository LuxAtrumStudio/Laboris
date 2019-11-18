const _ = require('lodash');
const dateParse = require('./dateparse.js');

parseQualifier = (argv) => {
  args = {
    'ref': (arg) => {
      return _.compact(_.filter(_.split(arg, ' '), (o) => {
        return !(o[0] == '-' ||
          o[0] == '+' ||
          o[0] == '@' ||
          o[0] == '_' ||
          _.startsWith(o, 'p:') ||
          _.startsWith(o, 'pri:') ||
          _.startsWith(o, 'priority:') ||
          _.startsWith(o, 'pgt:') ||
          _.startsWith(o, 'prigt:') ||
          _.startsWith(o, 'prioritygt:') ||
          _.startsWith(o, 'plt:') ||
          _.startsWith(o, 'prilt:') ||
          _.startsWith(o, 'prioritylt:') ||
          _.startsWith(o, 'pge:') ||
          _.startsWith(o, 'prige:') ||
          _.startsWith(o, 'priorityge:') ||
          _.startsWith(o, 'pgle:') ||
          _.startsWith(o, 'prile:') ||
          _.startsWith(o, 'priorityle:') ||
          _.startsWith(o, 'entry:') ||
          _.startsWith(o, 'entryDate:') ||
          _.startsWith(o, 'entryAfter:') ||
          _.startsWith(o, 'entryDateAfter:') ||
          _.startsWith(o, 'entryBefore:') ||
          _.startsWith(o, 'entryDateBefore:') ||
          _.startsWith(o, 'due:') ||
          _.startsWith(o, 'dueDate:') ||
          _.startsWith(o, 'dueAfter:') ||
          _.startsWith(o, 'dueDateAfter:') ||
          _.startsWith(o, 'dueBefore:') ||
          _.startsWith(o, 'dueDateBefore:') ||
          _.startsWith(o, 'done:') ||
          _.startsWith(o, 'doneDate:') ||
          _.startsWith(o, 'doneAfter:') ||
          _.startsWith(o, 'doneDateAfter:') ||
          _.startsWith(o, 'doneBefore:') ||
          _.startsWith(o, 'doneDateBefore:') ||
          _.startsWith(o, 'modified:') ||
          _.startsWith(o, 'modifiedDate:') ||
          _.startsWith(o, 'modifiedAfter:') ||
          _.startsWith(o, 'modifiedDateAfter:') ||
          _.startsWith(o, 'modifiedBefore:') ||
          _.startsWith(o, 'modifiedDateBefore:'));
      }));
    },
    'state': (arg) => {
      return arg.match(/\s--closed/) !== null ? false : arg.match(/\s--open/) ? true : null;
    },
    'priority': (arg) => {
      const res = arg.match(/(?<=\s(p:|pri:|priority:|-p=?|--pri=?|--priority=?))\s?(-?\d+)/);
      if (res) return _.toInteger(res[2]);
      return null;
    },
    'priority_gt': (arg) => {
      const res = arg.match(/(?<=\s(pgt:|prigt:|prioritygt:|-pgt=?|--prigt=?|--prioritygt=?))\s?(-?\d+)/);
      if (res) return _.toInteger(res[2]);
      return null;
    },
    'priority_lt': (arg) => {
      const res = arg.match(/(?<=\s(plt:|prilt:|prioritylt:|-plt=?|--prilt=?|--prioritylt=?))\s?(-?\d+)/);
      if (res) return _.toInteger(res[2]);
      return null;
    },
    'priority_ge': (arg) => {
      const res = arg.match(/(?<=\s(pge:|prige:|priorityge:|-pge=?|--prige=?|--priorityge=?))\s?(-?\d+)/);
      if (res) return _.toInteger(res[2]);
      return null;
    },
    'priority_le': (arg) => {
      const res = arg.match(/(?<=\s(ple:|prile:|priorityle:|-ple=?|--prile=?|--priorityle=?))\s?(-?\d+)/);
      if (res) return _.toInteger(res[2]);
      return null;
    },
    'hidden': (arg) => {
      return arg.match(/\s--hidden/) !== null ? true : null;
    },
    'entryDate': (arg) => {
      const res = arg.match(/(?<=\s(entry:|entryDate:|--entry=?|--entryDate=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'entryDateAfter': (arg) => {
      const res = arg.match(/(?<=\s(entryAfter:|entryDateAfter:|--entryAfter=?|--entryDategtAfter=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'entryDateBefore': (arg) => {
      const res = arg.match(/(?<=\s(entryBefore:|entryDateBefore:|--entryBefore=?|--entryDateBefore=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'dueDate': (arg) => {
      const res = arg.match(/(?<=\s(due:|dueDate:|--due=?|--dueDate=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'dueDateAfter': (arg) => {
      const res = arg.match(/(?<=\s(dueAfter:|dueDateAfter:|--dueAfter=?|--dueDateAfter=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'dueDateBefore': (arg) => {
      const res = arg.match(/(?<=\s(dueBefore:|dueDateBefore:|--dueBefore=?|--dueDateBefore=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'doneDate': (arg) => {
      const res = arg.match(/(?<=\s(done:|doneDate:|--done=?|--doneDate=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'doneDateAfter': (arg) => {
      const res = arg.match(/(?<=\s(doneAfter:|doneDateAfter:|--doneAfter=?|--doneDateAfter=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'doneDateBefore': (arg) => {
      const res = arg.match(/(?<=\s(doneBefore:|doneDateBefore:|--doneBefore=?|--doneDateBefore=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'modifiedDate': (arg) => {
      const res = arg.match(/(?<=\s(modified:|modifiedDate:|--modified=?|--modifiedDate=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'modifiedDateAfter': (arg) => {
      const res = arg.match(/(?<=\s(modifiedAfter:|modifiedDateAfter:|--modifiedAfter=?|--modifiedDateAfter=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'modifiedDateBefore': (arg) => {
      const res = arg.match(/(?<=\s(modifiedBefore:|modifiedDateBefore:|--modifiedBefore=?|--modifiedDateBefore=?))\s?(.+)/);
      if (res) return dateParse.parseDate(res[2]);
      return null;
    },
    'parents': (arg) => {
      const res = _.map(_.filter(_.split(arg, ' '), (o) => {
        return o[0] == '+';
      }), (o) => o.substr(1));
      return (res.length !== 0) ? res : null;
    },
    'children': (arg) => {
      const res = _.map(_.filter(_.split(arg, ' '), (o) => {
        return o[0] == '_';
      }), (o) => o.substr(1));
      return (res.length !== 0) ? res : null;
    },
    'tags': (arg) => {
      const res = _.map(_.filter(_.split(arg, ' '), (o) => {
        return o[0] == '@';
      }), (o) => o.substr(1));
      return (res.length !== 0) ? res : null;
    }
  };
  const args_str = ' ' + _.join(argv, ' ');
  for (const key in args) {
    args[key] = args[key](args_str);
  }
  return _.omitBy(args, _.isNil);
}
parseStart = (argv) => {
  return {
    "nargs": argv,
    "ref": argv[0],
  }
}
parseStop = (argv) => {
  return {
    "nargs": argv,
    "ref": _.join(argv, ' ')
  }
}
parseCreate = (argv) => {
  return {
    "nargs": argv,
    ...parseQualifier(argv)
  }
}
parseDelete = (argv) => {
  return {
    "nargs": argv,
    "ref": _.join(argv, ' ')
  }
}
parseOpen = (argv) => {
  return {
    "nargs": argv "ref": _.join(argv, ' ')
  }
}
parseClose = (argv) => {
  return {
    "nargs": argv "ref": _.join(argv, ' ')
  }
}

module.exports.parseArgs = () => {
  argv = _.slice(process.argv, 2);
  parsers = {
    "start": parseStart,
    "stop": parseStop,
    "create": parseCreate,
    "add": parseCreate,
    "new": parseCreate,
    "delete": parseDelete,
    "open": parseOpen,
    "close": parseClose,
    "list": parseQualifier,
  };
  if (argv.length === 0)
    return {
      'action': 'list'
    };
  if (argv[0].match(/^(-h|--help)$/)) {
    return {
      'action': 'help',
      'module': 'root'
    };
  }
  for (const key in parsers) {
    if (argv[0] == key)
      return {
        'action': argv[0],
        ...parsers[key](_.slice(argv, 1))
      };
  }
  return {
    'action': 'list',
    ...parseQualifier(argv)
  };
};
