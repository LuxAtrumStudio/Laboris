const _ = require("lodash");
const chalk = require("chalk");

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
  else if (diff[2] > 0) return diff[2] + "m";
  else if (diff[3] > 0) return diff[3] + "s";
  else return "NOW";
};

module.exports.dateDeltaMin = (a, b) => {
  const diff = this.dateDelta(a, b);
  if (diff[0] > 0)
    return diff[0] + "w " + diff[1] + "d " + diff[2] + "m " + diff[3] + "s";
  else if (diff[1] > 0) return diff[1] + "d " + diff[2] + "m " + diff[3] + "s";
  else if (diff[2] > 0) return diff[2] + "m " + diff[3] + "s";
  else if (diff[3] > 0) return diff[3] + "s";
  else return "NOW";
};

module.exports.dateDeltaFull = (a, b) => {
  const diff = this.dateDelta(a, b);
  return diff[0] + "w " + diff[1] + "d " + diff[2] + "m " + diff[3] + "s";
};

module.exports.short = task => {
  var msg = task._id.slice(0, 4) + " " + task.title;
  if (task.tags.length !== 0)
    msg += chalk.yellow.bold(" @" + _.join(task.tags, " @"));
  if (task.parents.length !== 0)
    msg += chalk.blue.bold(" +" + _.join(task.parents, " @"));
  if (task.dueDate) msg += " " + this.dateDeltaMajor(Date.now(), task.dueDate);
  return msg;
};
