const _ = require('lodash');
const tinygradient = require('tinygradient');

const calcUrgDueDate = (task) => {
  if (task.dueDate === null) return 0.0;
  const daysDue = (_.now() - task.dueDate) / 86400000;
  const totalActive = (task.dueDate - task.entryDate) / 86400000;
  const a = -4.39449 / totalActive;
  const b = -2.19722 / 1;
  return 1.0 / (1 + Math.exp(a * (daysDue + b)));
};

module.exports.calcUrg = (task) => {
  if (task.priority === 0 || task.doneDate !== null) return 0.0;
  var urg = 0.0;
  urg += Math.abs((0.01429 * (_.now() - task.entryDate)) / 86400000);
  urg += Math.abs(9.0 * calcUrgDueDate(task));
  urg += Math.abs(1.0 * task.parents.length);
  urg += Math.abs(0.2 * task.children.length);
  urg += Math.abs(0.2 * task.tags.length);
  urg += Math.abs(0.5 * (task.users.length - 1));
  urg += Math.abs(-2.0 * task.priority + 10);
  urg += Math.abs(4.0 * (task.times.length % 2 == 1));
  return urg;
};

module.exports.getUrgColor = (config, urg) => {
  console.log(config.get('urgColor'));
  const colors = tinygradient(config.get('urgColor')).hsv(10);
  console.log(colors);
  return '#ff00ff';
};

module.exports.splitDelta = (diff, components = {
  weeks: null,
  days: null,
  hours: null,
  minutes: null,
  seconds: null
}) => {
  if (components.months !== undefined) {
    components.months = Math.floor(diff / 2.628e9);
    diff -= components.months * 2.628e9;
  }
  if (components.weeks !== undefined) {
    components.weeks = Math.floor(diff / 6.048e8);
    diff -= components.weeks * 6.048e8;
  }
  if (components.days !== undefined) {
    components.days = Math.floor(diff / 8.64e7);
    diff -= components.days * 8.64e7;
  }
  if (components.hours !== undefined) {
    components.hours = Math.floor(diff / 3.6e6);
    diff -= components.hours * 3.6e6;
  }
  if (components.minutes !== undefined) {
    components.minutes = Math.floor(diff / 6e4);
    diff -= components.minutes * 6e4;
  }
  if (components.seconds !== undefined) {
    components.seconds = Math.floor(diff / 1e3);
    diff -= components.seconds * 1e3;
  }
};
module.exports.formatDelta = (diff, fmt = 'hh:mm:ss') => {
  components = {};
  if (fmt.includes('M')) components.months = null;
  if (fmt.includes('W')) components.weeks = null;
  if (fmt.includes('D')) components.days = null;
  if (fmt.includes('h')) components.hours = null;
  if (fmt.includes('m')) components.minutes = null;
  if (fmt.includes('s')) components.seconds = null;
  components = this.splitDelta(diff);
  fmt = fmt.replace('MM', _.toString(components.months).padStart(2, '0'));
  fmt = fmt.replace('M', _.toString(components.months));
  fmt = fmt.replace('WW', _.toString(components.weeks).padStart(2, '0'));
  fmt = fmt.replace('W', _.toString(components.weeks));
  fmt = fmt.replace('DD', _.toString(components.days).padStart(2, '0'));
  fmt = fmt.replace('D', _.toString(components.days));
  fmt = fmt.replace('hh', _.toString(components.hours).padStart(2, '0'));
  fmt = fmt.replace('h', _.toString(components.hours));
  fmt = fmt.replace('mm', _.toString(components.minutes).padStart(2, '0'));
  fmt = fmt.replace('m', _.toString(components.minutes));
  fmt = fmt.replace('ss', _.toString(components.seconds).padStart(2, '0'));
  fmt = fmt.replace('s', _.toString(components.seconds));
  return fmt;
};
