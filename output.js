const _ = require("lodash");
const chalk = require("chalk");

const wrapStr = (str, len = 80, prepend = 0) => {
  str = str.split(" ");
  res = "";
  line = "";
  for (id in str) {
    if ((line + str[id]).length > len) {
      res += line + "\n";
      line = " ".repeat(prepend);
    }
    line += str[id] + " ";
  }
  res += line;
  return res;
};

const calcUrgDueDate = tsk => {
  if (!tsk.dueDate) return 0.0;
  const daysDue = (_.now() - tsk.dueDate) / 86400000;
  const totalActive = (tsk.dueDate - tsk.entryDate) / 86400000;
  const a = -4.39449 / totalActive;
  const b = -2.19722 / a;
  return 1.0 / (1 + Math.exp(a * (daysDue + b)));
};

const calcUrg = tsk => {
  if (tsk.priority === 0 || tsk.doneDate !== null) return 0.0;
  var urg = 0.0;
  urg += Math.abs((0.01429 * (_.now() - tsk.entryDate)) / 86400000);
  urg += Math.abs(9.0 * calcUrgDueDate(tsk));
  urg += Math.abs(1.0 * tsk.parents.length);
  urg += Math.abs(0.5 * tsk.children.length);
  urg += Math.abs(0.2 * tsk.tags.length);
  urg += Math.abs(0.5 * (tsk.users.length - 1));
  urg += Math.abs(-2.0 * tsk.priority + 10);
  urg += Math.abs(4.0 * (tsk.times.length % 2 == 1));
  return urg;
};

const getUrgColor = (tsk, urg) => {
  if (tsk.times.length % 2 == 1) return chalk.bgGreen.black.bold;
  else if (urg >= 10.0) return chalk.red.bold.underline;
  else if (urg >= 9.5) return chalk.red.bold;
  else if (urg >= 9.0) return chalk.red;
  else if (urg >= 7.0) return chalk.yellow;
  else if (urg >= 5.0) return chalk.green;
  else if (urg >= 3.0) return chalk.blue;
  else return chalk;
};

const dateDelta = (a, b) => {
  var diff = 0;
  if (a > b) diff = a - b;
  else if (b === undefined) diff = a;
  else diff = b - a;
  const weeks = Math.floor(diff / 604800000);
  diff -= weeks * 604800000;
  const days = Math.floor(diff / 86400000);
  diff -= days * 86400000;
  const hours = Math.floor(diff / 3600000);
  diff -= hours * 3600000;
  const minutes = Math.floor(diff / 60000);
  diff -= minutes * 60000;
  const seconds = Math.floor(diff / 1000);
  diff -= seconds * 1000;
  if (a > b) return [-weeks, -days, -hours, -minutes, -seconds, -diff];
  else return [weeks, days, hours, minutes, seconds, diff];
};

const dateDeltaMajor = (a, b) => {
  const diff = dateDelta(a, b);
  if (diff[0] !== 0) return diff[0] + "w";
  else if (diff[1] !== 0) return diff[1] + "d";
  else if (diff[2] !== 0) return diff[2] + "h";
  else if (diff[3] !== 0) return diff[3] + "m";
  else return "NOW";
};

module.exports.fmtHelp = cmd => {
  console.log(cmd.usage, "\n\nOptions:");
  let longest = 0;
  for (const key in cmd) {
    if (key == "usage") continue;
    longest = Math.max(longest, key.length);
  }
  for (const key in cmd) {
    if (key == "usage") continue;
    console.log(
      wrapStr(
        "  " + key + " ".repeat(longest - key.length) + "  " + cmd[key],
        60,
        longest + 6
      )
    );
  }
};

module.exports.printTask = tsk => {
  // console.log(tsk);
  const urg = calcUrg(tsk);
  const urgColor = getUrgColor(tsk, urg);
  var msg = urgColor(tsk.uuid.slice(0, 4) + "  " + tsk.priority.toString());
  if (tsk.dueDate) {
    msg += "  " + urgColor(dateDeltaMajor(_.now(), tsk.dueDate));
  }
  msg += "  " + urgColor(tsk.title);
  if (tsk.tags.length !== 0) {
    msg += "  " + chalk.yellow.bold("@" + _.join(tsk.tags, " @"));
  }
  if (tsk.parents.length !== 0) {
    msg += "  " + chalk.blue.bold("+" + _.join(tsk.parents, " +"));
  }
  msg += "  " + urgColor(urg.toFixed(3));
  console.log(msg);
};

module.exports.error = msg => {
  console.log(chalk.red.bold(wrapStr("  ERROR: " + msg, 60, 9)));
};
module.exports.msg = msg => {
  console.log(chalk.cyan.bold(wrapStr("  " + msg, 60, 2)));
};
