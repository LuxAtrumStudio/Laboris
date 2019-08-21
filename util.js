const _ = require("lodash");
const moment = require("moment");

module.exports.wrap = (txt, padding, firstLine = true, width = 80) => {
  if (txt.length + padding > width) {
    words = txt.split(" ");
    txt = "";
    line = " ".repeat(padding);
    for (const id in words) {
      if (line.length + words[id].length > width) {
        txt += "\n" + line.slice(1);
        line = " ".repeat(padding);
      } else {
        line += " " + words[id];
      }
    }
    txt += "\n" + line.slice(1);
    if (firstLine === true) {
      return txt.slice(1);
    } else {
      return txt.slice(padding + 1);
    }
  } else if (firstLine === true) {
    return txt.padStart(padding);
  } else {
    return txt;
  }
};

module.exports.printHelp = (usage, description, args) => {
  console.log("laboris " + usage);

  if (description) {
    console.log("\n" + this.wrap(description, 2, true, 78) + "\n");
  }

  const keyLength = _.maxBy(Object.keys(args), k => k.length).length;
  for (const key in args) {
    help = this.wrap(args[key], keyLength + 4, false);
    console.log("  " + key.padEnd(keyLength) + "  " + help);
  }
};

module.exports.parseDate = str => {
  if (_.startsWith(str, "due:")) {
    str = str.slice(4);
  }

  dateFormats = [
    "",
    "DD-MM-YYYY",
    "MM-DD-YYYY",
    "DD-MM-YY",
    "MM-DD-YY",
    "DD-MM",
    "MM-DD",
    "DD",
    "ddd",
    "dddd"
  ];

  timeFormats = [
    "",
    "hh:MM:SS A",
    "hh:MM:SSA",
    "hh:MM A",
    "hh:MMA",
    "hh A",
    "hhA",
    "HH:MM:SS",
    "HH:MM",
    "HH"
  ];

  validFormats = [
    "DD-MM-YYYY",
    "DD-MM-YYYYThh:MM:SS A",
    "DD-MM-YYYYThh:MM:SSA",
    "DD-MM-YYYYThh:MM A",
    "DD-MM-YYYYThh:MMA",
    "DD-MM-YYYYThh A",
    "DD-MM-YYYYThhA",
    "DD-MM-YYYYTHH:MM:SS",
    "DD-MM-YYYYTHH:MM",
    "DD-MM-YYYYTHH",
    "MM-DD-YYYY",
    "MM-DD-YYYYThh:MM:SS A",
    "MM-DD-YYYYThh:MM:SSA",
    "MM-DD-YYYYThh:MM A",
    "MM-DD-YYYYThh:MMA",
    "MM-DD-YYYYThh A",
    "MM-DD-YYYYThhA",
    "MM-DD-YYYYTHH:MM:SS",
    "MM-DD-YYYYTHH:MM",
    "MM-DD-YYYYTHH",
    "DD-MM-YY",
    "DD-MM-YYThh:MM:SS A",
    "DD-MM-YYThh:MM:SSA",
    "DD-MM-YYThh:MM A",
    "DD-MM-YYThh:MMA",
    "DD-MM-YYThh A",
    "DD-MM-YYThhA",
    "DD-MM-YYTHH:MM:SS",
    "DD-MM-YYTHH:MM",
    "DD-MM-YYTHH",
    "MM-DD-YY",
    "MM-DD-YYThh:MM:SS A",
    "MM-DD-YYThh:MM:SSA",
    "MM-DD-YYThh:MM A",
    "MM-DD-YYThh:MMA",
    "MM-DD-YYThh A",
    "MM-DD-YYThhA",
    "MM-DD-YYTHH:MM:SS",
    "MM-DD-YYTHH:MM",
    "MM-DD-YYTHH",
    "DD-MM",
    "DD-MMThh:MM:SS A",
    "DD-MMThh:MM:SSA",
    "DD-MMThh:MM A",
    "DD-MMThh:MMA",
    "DD-MMThh A",
    "DD-MMThhA",
    "DD-MMTHH:MM:SS",
    "DD-MMTHH:MM",
    "DD-MMTHH",
    "MM-DD",
    "MM-DDThh:MM:SS A",
    "MM-DDThh:MM:SSA",
    "MM-DDThh:MM A",
    "MM-DDThh:MMA",
    "MM-DDThh A",
    "MM-DDThhA",
    "MM-DDTHH:MM:SS",
    "MM-DDTHH:MM",
    "MM-DDTHH",
    "DD",
    "DDThh:MM:SS A",
    "DDThh:MM:SSA",
    "DDThh:MM A",
    "DDThh:MMA",
    "DDThh A",
    "DDThhA",
    "DDTHH:MM:SS",
    "DDTHH:MM",
    "DDTHH",
    "ddd",
    "dddThh:MM:SS A",
    "dddThh:MM:SSA",
    "dddThh:MM A",
    "dddThh:MMA",
    "dddThh A",
    "dddThhA",
    "dddTHH:MM:SS",
    "dddTHH:MM",
    "dddTHH",
    "dddd",
    "ddddThh:MM:SS A",
    "ddddThh:MM:SSA",
    "ddddThh:MM A",
    "ddddThh:MMA",
    "ddddThh A",
    "ddddThhA",
    "ddddTHH:MM:SS",
    "ddddTHH:MM",
    "ddddTHH",
    "hh:MM:SS A",
    "hh:MM:SSA",
    "hh:MM A",
    "hh:MMA",
    "hh A",
    "hhA",
    "HH:MM:SS",
    "HH:MM",
    "HH"
  ];

  const res = moment(str, validFormats);
  if (!res.isValid()) {
    return undefined;
  }
  return res.valueOf();
};

module.exports.urgDueDate = task => {
  if (!task.dueDate) return 0.0;
  const daysDue = (Date.now() - task.dueDate) / 86400000;
  const totalActive = (task.dueDate - task.entryDate) / 86400000;
  const a = -4.39449 / totalActive;
  const b = -2.19722 / a;
  return 1.0 / (1 + Math.exp(a * (daysDue + b)));
};

module.exports.urg = (task, config) => {
  if (task.priority === 0) return 0.0;
  var urg = 0.0;
  urg += Math.abs(
    parseFloat(config.get("urgency.age")) *
      ((Date.now() - task.entryDate) / 86400000)
  );
  urg += Math.abs(
    parseFloat(config.get("urgency.due")) * this.urgDueDate(task)
  );
  urg += Math.abs(
    parseFloat(config.get("urgency.parents")) * task.parents.length
  );
  urg += Math.abs(
    parseFloat(config.get("urgency.children")) * task.children.length
  );
  urg += Math.abs(parseFloat(config.get("urgency.tags")) * task.tags.length);
  urg += Math.abs(
    parseFloat(config.get("urgency.priority")) * task.priority + 10
  );
  urg += Math.abs(
    parseFloat(config.get("urgency.active")) * task.times.length !== 0 &&
      _.last(task.times).length === 1
      ? 1.0
      : 0.0
  );
  return urg;
};

module.exports.fmt = (fmt, data) => {
  data = data[fmt.key];
  if (data === undefined) return "undefined";
  if (fmt.type) {
    if (fmt.type === "f")
      data = fmt.precision
        ? parseFloat(data).toFixed(fmt.precision)
        : parseFloat(data).toString();
    else if (fmt.type === "d") data = parseInt(data).toString();
  } else data = data.toString();
  if (fmt.width) {
    if (data.length > fmt.width) {
      if (fmt.wrap === "-")
        data =
          fmt.width >= 10
            ? data.slice(0, fmt.width - 3) + "..."
            : data.slice(0, fmt.width);
      else if (fmt.wrap === "+") data = data;
    } else if (data.length < fmt.width) {
      if (fmt.align === "<") data = data + " ".repeat(fmt.width - data.length);
      else if (fmt.align === ">")
        data = " ".repeat(fmt.width - data.length) + data;
      else if (fmt.align === "^")
        data =
          " ".repeat(Math.ceil((fmt.width - data.length) / 2.0)) +
          data +
          " ".repeat(Math.floor((fmt.width - data.length) / 2.0));
      else data = " ".repeat(fmt.width - data.length) + data;
    }
  }
  return data;
};
