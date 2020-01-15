const _ = require('lodash');
const datetime = require('./datetime.js');

const cliUtil = require('./cliUtil.js');

const parseRef = (argv) => {
  return '', argv;
};
const parseParents = (argv) => {
  parents = [];
  newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      parents.push(arg);
      skipNext = false;
      continue;
    }
    if (arg[0] === '+')
      parents.push(arg.slice(1));
    else if (arg.match(/^--parent=/))
      parents.push(arg.slice(9));
    else if (arg.match(/^--parents=/))
      parents.push(arg.slice(10));
    else if (arg.match(/^--parent$/))
      skipNext = true;
    else if (arg.match(/^--parents$/))
      skipNext = true;
    else
      newArgv.push(arg);
  }
  return [parents, newArgv];
};
const parseChildren = (argv) => {
  children = [];
  newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      children.push(arg);
      skipNext = false;
      continue;
    }
    if (arg[0] === '%')
      children.push(arg.slice(1));
    else if (arg.match(/^--child=/))
      children.push(arg.slice(8));
    else if (arg.match(/^--children=/))
      children.push(arg.slice(11));
    else if (arg.match(/^--child$/))
      skipNext = true;
    else if (arg.match(/^--children$/))
      skipNext = true;
    else
      newArgv.push(arg);
  }
  return [children, newArgv];
};
const parseTags = (argv) => {
  tags = [];
  newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      tags.push(arg);
      skipNext = false;
      continue;
    }
    if (arg[0] === '@')
      tags.push(arg.slice(1));
    else if (arg.match(/^--tag=/))
      tags.push(arg.slice(6));
    else if (arg.match(/^--tags=/))
      tags.push(arg.slice(7));
    else if (arg.match(/^--tag$/))
      skipNext = true;
    else if (arg.match(/^--tags$/))
      skipNext = true;
    else
      newArgv.push(arg);
  }
  return [tags, newArgv];
};
const parseDate = (short, long, argv) => {
  let date = null;
  let newArgv = [];
  let skipNext = false;
  shortInline = new RegExp('^' + short + ':');
  longInline = new RegExp('^' + long + ':');
  shortCapture = new RegExp('^--' + short + '=');
  longCapture = new RegExp('^--' + long + '=');
  shortSkip = new RegExp('^--' + short + '$');
  longSkip = new RegExp('^--' + long + '$');
  for (const arg of argv) {
    if (skipNext) {
      date = arg;
      skipNext = false;
      continue;
    }
    if (arg.match(shortInline))
      date = arg.slice(short.length + 1);
    else if (arg.match(longInline))
      date = arg.slice(long.length + 1);
    else if (arg.match(shortCapture))
      date = arg.slice(short.length + 3);
    else if (arg.match(longCapture))
      date = arg.slice(long.length + 3);
    else if (arg.match(shortSkip))
      skipNext = true;
    else if (arg.match(longSkip))
      skipNext = true;
    else
      newArgv.push(arg);
  }
  return [(date !== null ? datetime.parse(date) : null), newArgv];
};
const parseDueDate = (argv) => {
  return parseDate('due', 'dueDate', argv);
};
const parseHidden = (argv) => {
  let hidden = false;
  let newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--hidden$/))
      hidden = true;
    else
      newArgv.push(arg);
  }
  return [hidden, newArgv];
};

const filterGenericNumber = (name, argv, defaultValue = undefined) => {
  let val = defaultValue;
  let newArgv = [];
  regexSkip = new RegExp('^--' + name + '$');
  regexCapture = new RegExp('^--' + name + '=');
  regexInline = new RegExp(name + ':');
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      skipNext = false;
      val = _.toInteger(arg);
      continue;
    }
    if (arg.match(regexInline))
      val = _.toInteger(arg.slice(name.length + 1));
    else if (arg.match(regexCapture))
      val = _.toInteger(arg.slice(name.length + 3));
    else if (arg.match(regexSkip))
      skipNext = true;
    else
      newArgv.push(arg);
  }
  return [val, newArgv];
};
const filterNumber = (names, argv, defaultValue = undefined) => {
  let val = defaultValue;
  for (const key of names) {
    [val, argv] = filterGenericNumber(key, argv, val);
  }
  return [val, argv];
};

const filterHidden = (argv) => {
  let hidden = false;
  let newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--hidden$/))
      hidden = true;
    else if (arg.match(/^--no-hidden$/))
      hidden = false;
    else if (arg.match(/^--all-hidden$/))
      hidden = undefined;
    else
      newArgv.push(arg);
  }
  return [hidden, newArgv];
};
const filterOpen = (argv) => {
  let open = true;
  let newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--open$/))
      open = true;
    else if (arg.match(/^--closed$/))
      open = true;
    else if (arg.match(/^--all$/))
      open = undefined;
    else
      newArgv.push(arg);
  }
  return [open, newArgv];
};
const filterActive = (argv) => {
  let active = true;
  let newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--active$/))
      active = true;
    else if (arg.match(/^--not-active$/))
      active = true;
    else if (arg.match(/^--all-active$/))
      active = undefined;
    else
      newArgv.push(arg);
  }
  return [active, newArgv];
};

const parseFilter = (argv) => {
  let filter = {};
  [filter.parents, argv] = parseParents(argv);
  [filter.children, argv] = parseChildren(argv);
  [filter.tags, argv] = parseTags(argv);
  [filter.open, argv] = filterOpen(argv);
  [filter.hidden, argv] = filterHidden(argv);
  [filter.active, argv] = filterActive(argv);
  [filter.priority, argv] = filterNumber(['pri', 'priority'], argv);
  [filter.priorityG, argv] = filterNumber(['priG', 'priorityG'], argv);
  [filter.priorityL, argv] = filterNumber(['priL', 'priorityL'], argv);
  [filter.parentCount, argv] = filterNumber(['parentCount'], argv);
  [filter.parentCountG, argv] = filterNumber(['parentCountG'], argv);
  [filter.parentCountL, argv] = filterNumber(['parentCountL'], argv);
  [filter.childCount, argv] = filterNumber(['childCount'], argv);
  [filter.childCountG, argv] = filterNumber(['childCountG'], argv);
  [filter.childCountL, argv] = filterNumber(['childCountL'], argv);
  [filter.tagCount, argv] = filterNumber(['tagCount'], argv);
  [filter.tagCountG, argv] = filterNumber(['tagCountG'], argv);
  [filter.tagCountL, argv] = filterNumber(['tagCountL'], argv);
  [filter.due, argv] = parseDate('due', 'dueDate', argv);
  [filter.dueBefore, argv] = parseDate('dueB', 'dueBefore', argv);
  [filter.dueAfter, argv] = parseDate('dueA', 'dueAfter', argv);
  [filter.entry, argv] = parseDate('entry', 'entryDate', argv);
  [filter.entryBefore, argv] = parseDate('entryB', 'entryBefore', argv);
  [filter.entryAfter, argv] = parseDate('entryA', 'entryAfter', argv);
  [filter.done, argv] = parseDate('done', 'doneDate', argv);
  [filter.doneBefore, argv] = parseDate('doneB', 'doneBefore', argv);
  [filter.doneAfter, argv] = parseDate('doneA', 'doneAfter', argv);
  [filter.modified, argv] = parseDate('modified', 'modifiedDate', argv);
  [filter.modifiedBefore, argv] =
      parseDate('modifiedB', 'modifiedDefore', argv);
  [filter.modifiedAfter, argv] = parseDate('modifiedA', 'modifiedAfter', argv);
  return [filter, argv];
};

const hasHelp =
    (argv) => {
      for (const arg of argv) {
        if (arg === '-h' || arg === '--help') return true;
      }
      return false;
    }

const parseCreate = (argv) => {
  let cmd = {command: 'create', args: {}};
  [cmd.args.parents, argv] = parseParents(argv);
  [cmd.args.children, argv] = parseChildren(argv);
  [cmd.args.tags, argv] = parseTags(argv);
  [cmd.args.dueDate, argv] = parseDueDate(argv);
  [cmd.args.hidden, argv] = parseHidden(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText(
        'Usage: laboris create TITLE... [+PARENT...] [%CHILD...] [@TAG...] [due:DATE] [--hidden]',
        80, 22);
    cliUtil.printTable(
        [
          ['TITLE', 'Task description'], ['PARENT', 'Parent tasks'],
          ['CHILD', 'Child tasks'], ['TAG', 'Task tags'],
          ['DATE', 'Optional task due date'],
          ['--hidden', 'Will hide the task by default']
        ],
        ['>', '<']);
    return undefined;
  }
  if (argv.length === 0) throw 'Parse Error[start]: Task title is required';
  cmd.args.ref = _.join(argv, ' ');
  return cmd;
};
const parseDelete = (argv) => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText('Usage: laboris delete TITLE... [FILTER_OPTIONS]', 80, 22);
    cliUtil.printTable([['TITLE', 'Task to delete']], ['>', '<']);
    return undefined;
  }
  if (argv.length === 0) throw 'Parse Error[start]: Task title is required';
  return cmd = {command: 'delete', args: {ref: _.join(argv, ' '), ...filter}};
};
const parseStart = (argv) => {
  let time = undefined;
  if (argv.length > 1) time = datetime.parse(_.last(argv));
  if (time) argv = _.slice(argv, 0, argv.length - 1);
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText(
        'Usage: laboris start TITLE... [FILTER_OPTIONS] [TIME]', 80, 22);
    cliUtil.printTable(
        [
          ['TITLE', 'Task to start tracking'],
          ['TIME', 'Optional start time, to start tracking the task at']
        ],
        ['>', '<']);
    return undefined;
  }
  if (argv.length === 0) throw 'Parse Error[start]: Task title is required';
  return cmd = {
    command: 'start',
    args: {
      time: time ? time : _.now(),
      ref: _.join(argv, ' '),
      ...filter,
      active: false
    }
  };
};
const parseStop = (argv) => {
  let time = undefined;
  if (argv.length > 1) time = datetime.parse(_.last(argv));
  if (time) argv = _.slice(argv, 0, argv.length - 1);
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText(
        'Usage: laboris stop TITLE... [FILTER_OPTIONS] [TIME]', 80, 22);
    cliUtil.printTable(
        [
          ['TITLE', 'Task to stop tracking'],
          ['TIME', 'Optional stop time, to stop tracking the task at']
        ],
        ['>', '<']);
    return undefined;
  }
  if (argv.length === 0) throw 'Parse Error[start]: Task title is required';
  return cmd = {
    command: 'stop',
    args: {
      time: time ? time : _.now(),
      ref: _.join(argv, ' '),
      ...filter,
      active: true
    }
  };
};
const parseClose = (argv) => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText('Usage: laboris close TITLE... [FILTER_OPTIONS]', 80, 22);
    cliUtil.printTable([['TITLE', 'Task to close']], ['>', '<']);
    return undefined;
  }
  if (argv.length === 0) throw 'Parse Error[start]: Task title is required';
  return cmd = {
    command: 'close',
    args: {ref: _.join(argv, ' '), ...filter, open: true}
  };
};
const parseOpen = (argv) => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText('Usage: laboris open TITLE... [FILTER_OPTIONS]', 80, 22);
    cliUtil.printTable([['TITLE', 'Task to open']], ['>', '<']);
    return undefined;
  }
  if (argv.length === 0) throw 'Parse Error[start]: Task title is required';
  return cmd = {
    command: 'open',
    args: {ref: _.join(argv, ' '), ...filter, open: false}
  };
};
const parseList = (argv) => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText('Usage: laboris list [FILTER_OPTIONS]', 80, 22);
    return undefined;
  }
  return cmd = {command: 'list', args: {ref: _.join(argv, ' '), ...filter}};
};

module.exports = (argv = undefined) => {
  return new Promise((resolve, reject) => {
    if (argv === undefined) argv = _.slice(process.argv, 2);
    if (argv.length > 0) {
      if (argv[0] === 'create')
        return resolve(parseCreate(_.slice(argv, 1)));
      else if (argv[0] === 'delete')
        return resolve(parseDelete(_.slice(argv, 1)));
      else if (argv[0] === 'start')
        return resolve(parseStart(_.slice(argv, 1)));
      else if (argv[0] === 'stop')
        return resolve(parseStop(_.slice(argv, 1)));
      else if (argv[0] === 'close')
        return resolve(parseClose(_.slice(argv, 1)));
      else if (argv[0] === 'open')
        return resolve(parseOpen(_.slice(argv, 1)));
      else if (argv[0] === 'list')
        return resolve(parseList(_.slice(argv, 1)));
    }
  });
}