const _ = require("lodash");
const datetime = require("./datetime.js");

const cliUtil = require("./cliUtil.js");

const parseRef = argv => {
  return "", argv;
};
const parseParents = argv => {
  parents = [];
  newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      parents.push(arg);
      skipNext = false;
      continue;
    }
    if (arg[0] === "+") parents.push(arg.slice(1));
    else if (arg.match(/^--parent=/)) parents.push(arg.slice(9));
    else if (arg.match(/^--parents=/)) parents.push(arg.slice(10));
    else if (arg.match(/^--parent$/)) skipNext = true;
    else if (arg.match(/^--parents$/)) skipNext = true;
    else newArgv.push(arg);
  }
  return [parents, newArgv];
};
const parseChildren = argv => {
  children = [];
  newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      children.push(arg);
      skipNext = false;
      continue;
    }
    if (arg[0] === "%") children.push(arg.slice(1));
    else if (arg.match(/^--child=/)) children.push(arg.slice(8));
    else if (arg.match(/^--children=/)) children.push(arg.slice(11));
    else if (arg.match(/^--child$/)) skipNext = true;
    else if (arg.match(/^--children$/)) skipNext = true;
    else newArgv.push(arg);
  }
  return [children, newArgv];
};
const parseTags = argv => {
  tags = [];
  newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      tags.push(arg);
      skipNext = false;
      continue;
    }
    if (arg[0] === "@") tags.push(arg.slice(1));
    else if (arg.match(/^--tag=/)) tags.push(arg.slice(6));
    else if (arg.match(/^--tags=/)) tags.push(arg.slice(7));
    else if (arg.match(/^--tag$/)) skipNext = true;
    else if (arg.match(/^--tags$/)) skipNext = true;
    else newArgv.push(arg);
  }
  return [tags, newArgv];
};
const parseDate = (short, long, argv) => {
  let date = undefined;
  const newArgv = [];
  let skipNext = false;
  shortInline = new RegExp("^" + short + ":");
  longInline = new RegExp("^" + long + ":");
  shortCapture = new RegExp("^--" + short + "=");
  longCapture = new RegExp("^--" + long + "=");
  shortSkip = new RegExp("^--" + short + "$");
  longSkip = new RegExp("^--" + long + "$");
  for (const arg of argv) {
    if (skipNext) {
      date = arg;
      skipNext = false;
      continue;
    }
    if (arg.match(shortInline)) date = arg.slice(short.length + 1);
    else if (arg.match(longInline)) date = arg.slice(long.length + 1);
    else if (arg.match(shortCapture)) date = arg.slice(short.length + 3);
    else if (arg.match(longCapture)) date = arg.slice(long.length + 3);
    else if (arg.match(shortSkip)) skipNext = true;
    else if (arg.match(longSkip)) skipNext = true;
    else newArgv.push(arg);
  }
  return [date !== null ? datetime.parse(date) : null, newArgv];
};
const parseDueDate = argv => {
  return parseDate("due", "dueDate", argv);
};
const parseHidden = argv => {
  let hidden = false;
  const newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--hidden$/)) hidden = true;
    else newArgv.push(arg);
  }
  return [hidden, newArgv];
};
const parsePriority = argv => {
  let priority = 5;
  const newArgv = [];
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      priority = _.toInteger(arg);
      skipNext = false;
      continue;
    }
    if (arg.match(/^p:/)) priority = _.toInteger(arg.slice(2));
    else if (arg.match(/^pri:/)) priority = _.toInteger(arg.slice(4));
    else if (arg.match(/^priority:/)) priority = _.toInteger(arg.slice(9));
    else if (arg.match(/^--pri=/)) priority = _.toInteger(arg.slice(6));
    else if (arg.match(/^--priority=/)) priority = _.toInteger(arg.slice(11));
    else if (arg.match(/^--pri$/)) skipNext = true;
    else if (arg.match(/^--priority$/)) skipNext = true;
    else newArgv.push(arg);
  }
  return [priority, newArgv];
};

const filterGenericNumber = (name, argv, defaultValue = undefined) => {
  let val = defaultValue;
  const newArgv = [];
  regexSkip = new RegExp("^--" + name + "$");
  regexCapture = new RegExp("^--" + name + "=");
  regexInline = new RegExp(name + ":");
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      skipNext = false;
      val = _.toInteger(arg);
      continue;
    }
    if (arg.match(regexInline)) val = _.toInteger(arg.slice(name.length + 1));
    else if (arg.match(regexCapture)) {
      val = _.toInteger(arg.slice(name.length + 3));
    } else if (arg.match(regexSkip)) skipNext = true;
    else newArgv.push(arg);
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

const filterHidden = argv => {
  let hidden = false;
  const newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--hidden$/)) hidden = true;
    else if (arg.match(/^--no-hidden$/)) hidden = false;
    else if (arg.match(/^--all-hidden$/)) hidden = undefined;
    else newArgv.push(arg);
  }
  return [hidden, newArgv];
};
const filterOpen = argv => {
  let open = true;
  const newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--open$/)) open = true;
    else if (arg.match(/^--closed$/)) open = true;
    else if (arg.match(/^--all$/)) open = undefined;
    else newArgv.push(arg);
  }
  return [open, newArgv];
};
const filterActive = argv => {
  let active = undefined;
  const newArgv = [];
  for (const arg of argv) {
    if (arg.match(/^--active$/)) active = true;
    else if (arg.match(/^--not-active$/)) active = true;
    else if (arg.match(/^--all-active$/)) active = undefined;
    else newArgv.push(arg);
  }
  return [active, newArgv];
};

const parseFilter = argv => {
  const filter = {};
  [filter.parents, argv] = parseParents(argv);
  [filter.children, argv] = parseChildren(argv);
  [filter.tags, argv] = parseTags(argv);
  [filter.open, argv] = filterOpen(argv);
  [filter.hidden, argv] = filterHidden(argv);
  [filter.active, argv] = filterActive(argv);
  [filter.priority, argv] = filterNumber(["pri", "priority"], argv);
  [filter.priorityG, argv] = filterNumber(["priG", "priorityG"], argv);
  [filter.priorityL, argv] = filterNumber(["priL", "priorityL"], argv);
  [filter.parentCount, argv] = filterNumber(["parentCount"], argv);
  [filter.parentCountG, argv] = filterNumber(["parentCountG"], argv);
  [filter.parentCountL, argv] = filterNumber(["parentCountL"], argv);
  [filter.childCount, argv] = filterNumber(["childCount"], argv);
  [filter.childCountG, argv] = filterNumber(["childCountG"], argv);
  [filter.childCountL, argv] = filterNumber(["childCountL"], argv);
  [filter.tagCount, argv] = filterNumber(["tagCount"], argv);
  [filter.tagCountG, argv] = filterNumber(["tagCountG"], argv);
  [filter.tagCountL, argv] = filterNumber(["tagCountL"], argv);
  [filter.due, argv] = parseDate("due", "dueDate", argv);
  [filter.dueBefore, argv] = parseDate("dueB", "dueBefore", argv);
  [filter.dueAfter, argv] = parseDate("dueA", "dueAfter", argv);
  [filter.entry, argv] = parseDate("entry", "entryDate", argv);
  [filter.entryBefore, argv] = parseDate("entryB", "entryBefore", argv);
  [filter.entryAfter, argv] = parseDate("entryA", "entryAfter", argv);
  [filter.done, argv] = parseDate("done", "doneDate", argv);
  [filter.doneBefore, argv] = parseDate("doneB", "doneBefore", argv);
  [filter.doneAfter, argv] = parseDate("doneA", "doneAfter", argv);
  [filter.modified, argv] = parseDate("modified", "modifiedDate", argv);
  [filter.modifiedBefore, argv] = parseDate(
    "modifiedB",
    "modifiedDefore",
    argv
  );
  [filter.modifiedAfter, argv] = parseDate("modifiedA", "modifiedAfter", argv);
  return [filter, argv];
};

const hasHelp = argv => {
  for (const arg of argv) {
    if (arg === "-h" || arg === "--help") return true;
  }
  return false;
};

const parseCreate = argv => {
  const cmd = {
    command: "create",
    args: {}
  };
  [cmd.args.parents, argv] = parseParents(argv);
  [cmd.args.children, argv] = parseChildren(argv);
  [cmd.args.tags, argv] = parseTags(argv);
  [cmd.args.dueDate, argv] = parseDueDate(argv);
  [cmd.args.hidden, argv] = parseHidden(argv);
  [cmd.args.priority, argv] = parsePriority(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText(
      "Usage: laboris create TITLE... [+PARENT...] [%CHILD...] [@TAG...] [p:PRIORITY] [due:DATE] [--hidden]",
      80,
      22
    );
    cliUtil.printTable(
      [
        ["TITLE", "Task description"],
        ["PARENT", "Parent tasks"],
        ["CHILD", "Child tasks"],
        ["TAG", "Task tags"],
        ["PRIORITY", "Task priority"],
        ["DATE", "Optional task due date"],
        ["--hidden", "Will hide the task by default"]
      ],
      [">", "<"]
    );
    return undefined;
  }
  if (argv.length === 0) throw "Parse Error[create]: Task title is required";
  cmd.args.ref = _.join(argv, " ");
  return cmd;
};
const parseDelete = argv => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris delete TITLE... [FILTER_OPTIONS]", 80, 22);
    cliUtil.printTable([["TITLE", "Task to delete"]], [">", "<"]);
    return undefined;
  }
  if (argv.length === 0) throw "Parse Error[delete]: Task title is required";
  return {
    command: "delete",
    args: {
      ref: _.join(argv, " "),
      ...filter
    }
  };
};
const parseStart = argv => {
  let time = undefined;
  if (argv.length > 1) time = datetime.parse(_.last(argv));
  if (time) argv = _.slice(argv, 0, argv.length - 1);
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText(
      "Usage: laboris start TITLE... [FILTER_OPTIONS] [TIME]",
      80,
      22
    );
    cliUtil.printTable(
      [
        ["TITLE", "Task to start tracking"],
        ["TIME", "Optional start time, to start tracking the task at"]
      ],
      [">", "<"]
    );
    return undefined;
  }
  if (argv.length === 0) throw "Parse Error[start]: Task title is required";
  return {
    command: "start",
    args: {
      time: time ? time : _.now(),
      ref: _.join(argv, " "),
      ...filter,
      active: false
    }
  };
};
const parseStop = argv => {
  let time = undefined;
  if (argv.length > 1) time = datetime.parse(_.last(argv));
  if (time) argv = _.slice(argv, 0, argv.length - 1);
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText(
      "Usage: laboris stop TITLE... [FILTER_OPTIONS] [TIME]",
      80,
      22
    );
    cliUtil.printTable(
      [
        ["TITLE", "Task to stop tracking"],
        ["TIME", "Optional stop time, to stop tracking the task at"]
      ],
      [">", "<"]
    );
    return undefined;
  }
  if (argv.length === 0) throw "Parse Error[stop]: Task title is required";
  return {
    command: "stop",
    args: {
      time: time ? time : _.now(),
      ref: _.join(argv, " "),
      ...filter,
      active: true
    }
  };
};
const parseClose = argv => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris close TITLE... [FILTER_OPTIONS]", 80, 22);
    cliUtil.printTable([["TITLE", "Task to close"]], [">", "<"]);
    return undefined;
  }
  if (argv.length === 0) throw "Parse Error[close]: Task title is required";
  return {
    command: "close",
    args: {
      ref: _.join(argv, " "),
      ...filter,
      open: true
    }
  };
};
const parseOpen = argv => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris open TITLE... [FILTER_OPTIONS]", 80, 22);
    cliUtil.printTable([["TITLE", "Task to open"]], [">", "<"]);
    return undefined;
  }
  if (argv.length === 0) throw "Parse Error[open]: Task title is required";
  return {
    command: "open",
    args: {
      ref: _.join(argv, " "),
      ...filter,
      open: false
    }
  };
};
const parseAutolist = argv => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris report autolist [FILTER_OPTIONS]", 80, 22);
    return undefined;
  }
  return {
    command: "report",
    report: "autolist",
    args: {
      ref: _.join(argv, " "),
      ...filter
    }
  };
};
const parseList = argv => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris report list [FILTER_OPTIONS]", 80, 22);
    return undefined;
  }
  return {
    command: "report",
    report: "list",
    args: {
      ref: _.join(argv, " "),
      ...filter
    }
  };
};
const parseDetail = argv => {
  [filter, argv] = parseFilter(argv);
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris report detail [FILTER_OPTIONS]", 80, 22);
    return undefined;
  }
  return {
    command: "report",
    report: "detail",
    args: {
      ref: _.join(argv, " "),
      ...filter
    }
  };
};

const parseReport = argv => {
  if (argv.length > 0) {
    if (argv[0] === "autolist") return parseAutolist(_.slice(argv, 1));
    if (argv[0] === "list") return parseList(_.slice(argv, 1));
    if (argv[0] === "detail") return parseDetail(_.slice(argv, 1));
  }
};

const parseUserCreate = argv => {
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris user create EMAIL PASSWORD", 80, 22);
    return undefined;
  }
  if (argv.length === 0)
    throw "Parse Error[user create]: User email is required";
  if (argv.length === 1)
    throw "Parse Error[user create]: User password is required";
  return {
    command: "user",
    action: "create",
    args: {
      email: argv[0],
      password: argv[1]
    }
  };
};

const parseUserSignin = argv => {
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris user signin EMAIL PASSWORD", 80, 22);
    return undefined;
  }
  if (argv.length === 0)
    throw "Parse Error[user signin]: User email is required";
  if (argv.length === 1)
    throw "Parse Error[user signin]: User password is required";
  return {
    command: "user",
    action: "signin",
    args: {
      email: argv[0],
      password: argv[1]
    }
  };
};

const parseUserSignout = argv => {
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris user signout", 80, 22);
    return undefined;
  }
  return {
    command: "user",
    action: "signout",
    args: {}
  };
};

const parseUser = argv => {
  if (argv.length > 0) {
    if (argv[0] === "create") return parseUserCreate(_.slice(argv, 1));
    if (argv[0] === "signin") return parseUserSignin(_.slice(argv, 1));
    if (argv[0] === "signout") return parseUserSignout(_.slice(argv, 1));
  }
};

const parseConfig = argv => {
  let set = {};
  let newArgv = [];
  regexSkip = new RegExp(/^--set$/);
  regexCapture = new RegExp(/^--set=/);
  regexInline = new RegExp(/^([^=:]+)[:=](.+)$/);
  let skipNext = false;
  for (const arg of argv) {
    if (skipNext) {
      skipNext = false;
      set[_.last(newArgv)] = arg;
      newArgv = _.dropRight(newArgv);
      continue;
    }
    if (arg.match(regexCapture)) {
      if (newArgv.length === 0)
        throw "Parse Error[config]: Expected config value key before set flag";
      set[_.last(newArgv)] = arg.slice(6);
      newArgv = _.dropRight(newArgv);
    } else if (arg.match(regexInline)) {
      set[arg.match(regexInline)[1]] = arg.match(regexInline)[2];
    } else if (arg.match(regexSkip)) {
      if (newArgv.length === 0)
        throw "Parse Error[config]: Expected config value key before set flag";
      skipNext = true;
    } else newArgv.push(arg);
  }
  if (skipNext) throw "Parse Error[config]: Expected value for set flag";
  if (hasHelp(newArgv)) {
    cliUtil.wrapText(
      "Usage: laboris config [KEY [--set VAL] [KEY [--set VAL]...]]",
      80,
      22
    );
    return undefined;
  }
  return {
    command: "config",
    args: {
      keys: newArgv,
      set: set
    }
  };
};

const parseSync = argv => {
  if (hasHelp(argv)) {
    cliUtil.wrapText("Usage: laboris sync", 80, 22);
    return undefined;
  }
  return {
    command: "sync",
    args: {
      open: _.indexOf(argv, "--no-open") === -1,
      closed: _.indexOf(argv, "--closed") !== -1
    }
  };
};

module.exports = (argv = undefined) => {
  return new Promise((resolve, reject) => {
    if (argv === undefined) argv = _.slice(process.argv, 2);
    if (argv.length > 0) {
      if (argv[0] === "create") return resolve(parseCreate(_.slice(argv, 1)));
      else if (argv[0] === "delete") {
        return resolve(parseDelete(_.slice(argv, 1)));
      } else if (argv[0] === "start") {
        return resolve(parseStart(_.slice(argv, 1)));
      } else if (argv[0] === "stop")
        return resolve(parseStop(_.slice(argv, 1)));
      else if (argv[0] === "close") {
        return resolve(parseClose(_.slice(argv, 1)));
      } else if (argv[0] === "open")
        return resolve(parseOpen(_.slice(argv, 1)));
      else if (argv[0] === "list") return resolve(parseList(_.slice(argv, 1)));
      else if (argv[0] === "detail") {
        return resolve(parseDetail(_.slice(argv, 1)));
      } else if (argv[0] === "report") {
        return resolve(parseReport(_.slice(argv, 1)));
      } else if (argv[0] === "user") {
        return resolve(parseUser(_.slice(argv, 1)));
      } else if (argv[0] === "config") {
        return resolve(parseConfig(_.slice(argv, 1)));
      } else if (argv[0] === "sync") {
        return resolve(parseSync(_.slice(argv, 1)));
      } else return resolve(parseAutolist(argv));
    } else {
      return resolve(parseAutolist(argv));
    }
  });
};
