const _ = require("lodash");
const chalk = require("chalk");
const moment = require("moment");

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

const dateDeltaHM = (a, b) => {
  var diff = 0;
  if (a > b) diff = a - b;
  else if (b === undefined) diff = a;
  else diff = b - a;
  const hours = Math.floor(diff / 3600000);
  diff -= hours * 3600000;
  const minutes = Math.floor(diff / 60000);
  diff -= minutes * 60000;
  const seconds = Math.floor(diff / 1000);
  diff -= seconds * 1000;
  if (a > b) return [-hours, -minutes, -seconds, -diff];
  else return [hours, minutes, seconds, diff];
};
const deltaToHMS = (diff) => {
  const hours = Math.floor(diff / 3600000);
  diff -= hours * 3600000;
  const minutes = Math.floor(diff / 60000);
  diff -= minutes * 60000;
  const seconds = Math.floor(diff / 1000);
  diff -= seconds * 1000;
  return hours.toString() + ":" + minutes.toString().padStart(2, '0') + ":" + seconds.toString().padStart(2, '0');
}

const dateDeltaHMFormat = (a, b) => {
  const diff = dateDeltaHM(a, b);
  return diff[0].toString() + ":" + diff[1].toString().padStart(2, '0');
}

const dateDeltaMajor = (a, b) => {
  const diff = dateDelta(a, b);
  if (diff[0] !== 0) return diff[0] + "w";
  else if (diff[1] !== 0) return diff[1] + "d";
  else if (diff[2] !== 0) return diff[2] + "h";
  else if (diff[3] !== 0) return diff[3] + "m";
  else return "NOW";
};

const formatTimePeriod = (a, b) => {
  if (b == undefined || b == null) b = _.now();
  am = moment(a);
  bm = moment(b);
  if (am.isSame(bm, 'day')) {
    return am.format("YYYY-MM-DD") + "  " + am.format("HH:mm - ") + bm.format("HH:mm") + "  [" + dateDeltaHMFormat(a, b) + "]";
  } else {
    return am.format("YYYY-MM-DD HH:mm - ") + bm.format("YYYY-MM-DD HH:mm") + "  [" + dateDeltaHMFormat(a, b) + "]";
  }
}

const printTable = (table) => {
  colWidth = [];
  for(const r in table) {
    for(const c in table[r]) {
      if(c >= colWidth.length)
        colWidth.push(table[r][c].length);
      else
        colWidth[c] = Math.max(colWidth[c], table[r][c].length);
    }
  }
  for(const r in table) {
    if(r % 2 == 0)
      console.log(chalk.bgBlack(chalk.bold(table[r][0].padStart(colWidth[0], ' ')) + '  ' + table[r][1].padEnd(colWidth[1], ' ')));
    else
      console.log(chalk.bold(table[r][0].padStart(colWidth[0], ' ')) + '  ' + table[r][1].padEnd(colWidth[1], ' '));
  }
}

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

module.exports.formatTask = tsk => {
  // console.log(tsk);
  const urg = calcUrg(tsk);
  const urgColor = getUrgColor(tsk, urg);
  var msg = urgColor(tsk.uuid.slice(0, 4) + "  " + tsk.priority.toString());
  if (tsk.dueDate) {
    msg += urgColor("  " + dateDeltaMajor(_.now(), tsk.dueDate));
  }
  msg += urgColor("  " + tsk.title);
  if (tsk.tags.length !== 0) {
    msg += chalk.yellow.bold("  @" + _.join(tsk.tags, " @"));
  }
  if (tsk.parents.length !== 0) {
    msg += chalk.blue.bold("  +" + _.join(tsk.parents, " +"));
  }
  msg += urgColor("  " + urg.toFixed(3));
  return msg;
};

module.exports.printTask = tsk => {
  console.log(this.formatTask(tsk));
};

module.exports.formatDetails = tsk => {
  const urg = calcUrg(tsk);
  const urgColor = getUrgColor(tsk, urg);
  table = [];
  table.push(["Title", tsk.title]);
  table.push(["UUID", tsk.uuid]);
  if (tsk.tags.length !== 0) {
    table.push(["Tags", tsk.tags[0]]);
    for (const id in tsk.tags) {
      if (id == 0) continue;
      table.push(["", tsk.tags[id]]);
    }
  }
  if (tsk.parents.length !== 0) {
    table.push(["Parents", tsk.parents[0]]);
    for (const id in tsk.parents) {
      if (id == 0) continue;
      table.push(["", tsk.parents[id]]);
    }
  }
  if (tsk.children.length !== 0) {
    table.push(["Children", tsk.children[0]]);
    for (const id in tsk.children) {
      if (id == 0) continue;
      table.push(["", tsk.children[id]]);
    }
  }
  table.push(["Priority", tsk.priority.toString()]);
  table.push(["Urgency", urg.toFixed(5)]);
  table.push(["Hidden", tsk.hidden ? "True" : "False"]);
  table.push(["State", tsk.state ? "Open" : "Close"]);
  table.push(["Entry Date", moment(tsk.entryDate).format("YYYY-MM-DD HH:mm:ss")]);
  table.push(["Modified Date", moment(tsk.modifiedDate).format("YYYY-MM-DD HH:mm:ss")]);
  if (tsk.dueDate !== null)
    table.push(["Due Date", moment(tsk.dueDate).format("YYYY-MM-DD HH:mm:ss")]);
  if (tsk.doneDate !== null)
    table.push(["Done Date", moment(tsk.dueDate).format("YYYY-MM-DD HH:mm:ss")]);
  if (tsk.times.length !== 0) {
    table.push(["Times", formatTimePeriod(tsk.times[0], tsk.times[1])]);
    let total = (tsk.times[1] ? tsk.times[1] : _.now()) - tsk.times[0];
    for (const ids in tsk.times) {
      const id = parseInt(ids);
      if (id == 0) continue;
      else if (id % 2 == 1) continue;
      total += (tsk.times[id + 1] ? tsk.times[id + 1] : _.now()) - tsk.times[id];
      table.push(["", formatTimePeriod(tsk.times[id], tsk.times[id + 1])]);
    }
    table.push(["Total Time", deltaToHMS(total)]);
  }
  return table;
};
module.exports.printDetails = tsk => {
  printTable(this.formatDetails(tsk));
};

module.exports.error = msg => {
  console.log(chalk.red.bold(wrapStr("  ERROR: " + msg, 60, 9)));
};
module.exports.msg = msg => {
  console.log(chalk.cyan.bold(wrapStr("  " + msg, 60, 2)));
};
