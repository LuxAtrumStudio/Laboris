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
