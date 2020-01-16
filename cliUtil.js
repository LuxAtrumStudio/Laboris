const _ = require("lodash");
const chalk = require("chalk");
const data = require("./data.js");
const moment = require("moment");
const config = require("./config.js");

const dispLength = str => {
  let len = 0;
  let state = 0;
  for (const i in str) {
    if (str[i] == "\u001b") state = 1;
    else if (str[i] == "m" && state == 1) state = 0;
    else if (state == 0) len += 1;
  }
  return len;
};

const padLeft = (str, len, char = " ") => {
  return char.repeat(len - dispLength(str)) + str;
};
const padRight = (str, len, char = " ") => {
  return str + char.repeat(len - dispLength(str));
};

module.exports.wrapText = (str, width = 80, indent = 2, initIndent = 0) => {
  str = str.split(" ");
  res = "";
  line = " ".repeat(initIndent);
  for (const word of str) {
    if (dispLength(line + word) > width) {
      res += line + "\n";
      line = " ".repeat(indent);
    }
    line += word + " ";
  }
  res += line;
  console.log(res);
};

module.exports.printTable = (table, alignment = [], zebra = false) => {
  let colWidth = [];
  for (const r in table) {
    for (const c in table[r]) {
      if (c >= colWidth.length) colWidth.push(dispLength(table[r][c]));
      else colWidth[c] = Math.max(colWidth[c], dispLength(table[r][c]));
    }
  }
  while (alignment.length < colWidth.length) {
    alignment.push("<");
  }
  for (const r in table) {
    let line = "";
    for (const c in table[r]) {
      if (c !== 0) line += "  ";
      if (alignment[c] === "<") line += padRight(table[r][c], colWidth[c]);
      else if (alignment[c] === ">") line += padLeft(table[r][c], colWidth[c]);
    }
    if (zebra && r % 2 == 0) console.log(chalk.bgBlack(line));
    else console.log(line);
  }
};

module.exports.getColorFunc = color => {
  let func = chalk;
  if (color.fg !== "" && _.isString(color.fg)) func = func.hex(color.fg);
  else if (color.fg !== "") func = func.hex(color.fg.toHex());
  if (color.bg !== "" && _.isString(color.bg)) func = func.bgHex(color.bg);
  else if (color.bg !== "") func = func.bgHex(color.bg.toHex());
  if (_.findIndex(color.attr, "bold") !== -1) func = func.bold;
  if (_.findIndex(color.attr, "underline") !== -1) func = func.underline;
  return func;
};

module.exports.taskFmt = (fmt, task) => {
  const colors = {
    urg: this.getColorFunc(config.getUrgColor(task.urg)),
    title: this.getColorFunc(config.getColor("title")),
    parent: this.getColorFunc(config.getColor("parent")),
    child: this.getColorFunc(config.getColor("child")),
    tag: this.getColorFunc(config.getColor("tag"))
  };
  const keys = {
    uuidShort: task.uuid.slice(0, 8),
    uuid: task.uuid,
    priority: task.priority.toString(),
    title: task.title,
    parents:
      task.parents.length !== 0
        ? "+" + _.join(_.map(task.parents, data.getTitle), " +")
        : "",
    children:
      task.children.length !== 0
        ? "%" + _.join(_.map(task.children, data.getTitle), " %")
        : "",
    tags: task.tags.length !== 0 ? "@" + _.join(task.tags, " @") : "",
    dueDate: task.dueDate
      ? moment(task.dueDate).format("YYYY-MM-DD HH:mmm:ss")
      : "",
    entryDate: moment(task.entryDate).format("YYYY-MM-DD HH:mm:ss"),
    doneDate: task.doneDate
      ? moment(task.doneDate).format("YYYY-MM-DD HH:mm:ss")
      : "",
    modifiedDate: moment(task.modifiedDate).format("YYYY-MM-DD HH:mm:ss"),
    urg: task.urg.toFixed(3)
  };
  for (const color in colors) {
    fmt = fmt.replace(
      new RegExp("{([^:{}]+):" + color + "Color}"),
      colors[color]("{$1}")
    );
  }
  for (const key in keys) {
    fmt = fmt.replace(new RegExp("{" + key + "}"), keys[key]);
  }
  return fmt;
};

module.exports.formatShort = task => {
  return this.taskFmt(config.get("shortFormat"), task);
};

module.exports.formatList = task => {
  const fmt = str => this.taskFmt(str, task);
  return _.map(this.taskFmt(config.get("listFormat"), task).split(","), fmt);
};
