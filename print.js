const _ = require("lodash");
const chalk = require("chalk");
const { urgColor, urg } = require("./util.js");

module.exports.urgColor = urg => {
  if (urg >= 10.0) return chalk.red.bold.underline;
  else if (urg >= 9.5) return chalk.red.bold;
  else if (urg >= 9.0) return chalk.red;
  else if (urg >= 7.0) return chalk.yellow;
  else if (urg >= 5.0) return chalk.green;
  else if (urg >= 3.0) return chalk.blue;
  else return msg => msg;
};

module.exports.dateDelta = (a, b) => {
  var diff = b - a;
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
  return [weeks, days, hours, minutes, seconds, diff];
};

module.exports.dateDeltaMajor = (a, b) => {
  const diff = this.dateDelta(a, b);
  if (diff[0] > 0) return diff[0] + "w";
  else if (diff[1] > 0) return diff[1] + "d";
  else if (diff[2] > 0) return diff[2] + "h";
  else if (diff[3] > 0) return diff[3] + "m";
  else return "NOW";
};

module.exports.dateDeltaMin = (a, b) => {
  const diff = this.dateDelta(a, b);
  if (diff[0] > 0)
    return diff[0] + "w " + diff[1] + "d " + diff[2] + "h " + diff[3] + "m";
  else if (diff[1] > 0) return diff[1] + "d " + diff[2] + "h " + diff[3] + "m";
  else if (diff[2] > 0) return diff[2] + "h " + diff[3] + "m";
  else if (diff[3] > 0) return diff[3] + "m";
  else return "NOW";
};

module.exports.dateDeltaFull = (a, b) => {
  const diff = this.dateDelta(a, b);
  return diff[0] + "w " + diff[1] + "d " + diff[2] + "h " + diff[3] + "m";
};

module.exports.duration = (a, b) => {
  var diff = b - a;
  const hours = Math.floor(diff / 3600000);
  diff -= hours * 3600000;
  const minutes = Math.floor(diff / 60000);
  diff -= minutes * 60000;
  const seconds = Math.floor(diff / 1000);
  diff -= seconds * 1000;
  return (
    hours.toString().padStart(2, "0") +
    ":" +
    minutes.toString().padStart(2, "0")
  );
};

module.exports.short = (task, config) => {
  var urgVal = task.urg || urg(task, config);
  var msg =
    "  " + task._id.slice(0, 4) + " " + this.urgColor(urgVal)(task.title);
  if (task.tags.length !== 0)
    msg += chalk.yellow.bold(" @" + _.join(task.tags, " @"));
  if (task.parents.length !== 0)
    msg += chalk.blue.bold(" +" + _.join(task.parents, " @"));
  if (task.dueDate) msg += " " + this.dateDeltaMajor(Date.now(), task.dueDate);
  msg += " " + urgVal;
  return msg;
};

module.exports.refName = task => {
  return task._id.slice(0, 8) + "  " + task.title;
};
