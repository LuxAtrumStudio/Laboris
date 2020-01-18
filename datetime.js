const _ = require("lodash");
const moment = require("moment");

const parseRelativeDate = str => {
  const res = moment();
  Array.from(str.matchAll(/([\+-])(\d*)([wdhms])/gim)).forEach(mod => {
    if (mod[2] === "") mod[2] = "1";
    if (mod[1] === "+") {
      res.add({
        weeks: mod[3] === "w" ? parseInt(mod[2]) : 0,
        days: mod[3] === "d" ? parseInt(mod[2]) : 0,
        hours: mod[3] === "h" ? parseInt(mod[2]) : 0,
        minutes: mod[3] === "m" ? parseInt(mod[2]) : 0,
        seconds: mod[3] === "s" ? parseInt(mod[2]) : 0
      });
    } else {
      res.subtract({
        weeks: mod[3] === "w" ? parseInt(mod[2]) : 0,
        days: mod[3] === "d" ? parseInt(mod[2]) : 0,
        hours: mod[3] === "h" ? parseInt(mod[2]) : 0,
        minutes: mod[3] === "m" ? parseInt(mod[2]) : 0,
        seconds: mod[3] === "s" ? parseInt(mod[2]) : 0
      });
    }
  });
  return res.valueOf();
};

module.exports.parse = str => {
  // TODO Error matching 19:06 as 2019-06-02T02:00:00.000Z. It seems to be using
  // the MM-DD format
  if (str === undefined) return undefined;
  if (typeof str === "number") {
    return str;
  } else if (str.match(/today/i)) {
    return moment()
      .set({ hour: 0, minute: 0, second: 0 })
      .valueOf();
  } else if (str.match(/tomorrow/i)) {
    return moment()
      .set({ hour: 0, minute: 0, second: 0 })
      .add({ days: 1 })
      .valueOf();
  } else if (str.match(/yesterday/i)) {
    return moment()
      .set({ hour: 0, minute: 0, second: 0 })
      .subtract({ days: 1 })
      .valueOf();
  } else if (str.match(/([\+-]\d*[wdhms])+/i)) return parseRelativeDate(str);

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
    "hh:mm:ss A",
    "hh:mm:ssA",
    "hh:mm A",
    "hh:mmA",
    "hh A",
    "hhA",
    "HH:mm:ss",
    "HH:mm",
    "HH"
  ];

  validFormats = [
    "YYYY-MM-DD",
    "YYYY-MM-DDThh:mm:ss A",
    "YYYY-MM-DDThh:mm:ssA",
    "YYYY-MM-DDThh:mm A",
    "YYYY-MM-DDThh:mmA",
    "YYYY-MM-DDThh A",
    "YYYY-MM-DDThhA",
    "YYYY-MM-DDTHH:mm:ss",
    "YYYY-MM-DDTHH:mm",
    "YYYY-MM-DDTHH",
    "DD-MM-YYYY",
    "DD-MM-YYYYThh:mm:ss A",
    "DD-MM-YYYYThh:mm:ssA",
    "DD-MM-YYYYThh:mm A",
    "DD-MM-YYYYThh:mmA",
    "DD-MM-YYYYThh A",
    "DD-MM-YYYYThhA",
    "DD-MM-YYYYTHH:mm:ss",
    "DD-MM-YYYYTHH:mm",
    "DD-MM-YYYYTHH",
    "MM-DD-YYYY",
    "MM-DD-YYYYThh:mm:ss A",
    "MM-DD-YYYYThh:mm:ssA",
    "MM-DD-YYYYThh:mm A",
    "MM-DD-YYYYThh:mmA",
    "MM-DD-YYYYThh A",
    "MM-DD-YYYYThhA",
    "MM-DD-YYYYTHH:mm:ss",
    "MM-DD-YYYYTHH:mm",
    "MM-DD-YYYYTHH",
    "DD-MM-YY",
    "DD-MM-YYThh:mm:ss A",
    "DD-MM-YYThh:mm:ssA",
    "DD-MM-YYThh:mmm A",
    "DD-MM-YYThh:mmA",
    "DD-MM-YYThh A",
    "DD-MM-YYThhA",
    "DD-MM-YYTHH:mm:ss",
    "DD-MM-YYTHH:mm",
    "DD-MM-YYTHH",
    "MM-DD-YY",
    "MM-DD-YYThh:mm:ss A",
    "MM-DD-YYThh:mm:ssA",
    "MM-DD-YYThh:mm A",
    "MM-DD-YYThh:mmA",
    "MM-DD-YYThh A",
    "MM-DD-YYThhA",
    "MM-DD-YYTHH:mm:ss",
    "MM-DD-YYTHH:mm",
    "MM-DD-YYTHH",
    "DD-MM",
    "DD-MMThh:mm:ss A",
    "DD-MMThh:mm:ssA",
    "DD-MMThh:mm A",
    "DD-MMThh:mmA",
    "DD-MMThh A",
    "DD-MMThhA",
    "DD-MMTHH:mm:ss",
    "DD-MMTHH:mm",
    "DD-MMTHH",
    "MM-DD",
    "MM-DDThh:mm:ss A",
    "MM-DDThh:mm:ssA",
    "MM-DDThh:mm A",
    "MM-DDThh:mmA",
    "MM-DDThh A",
    "MM-DDThhA",
    "MM-DDTHH:mm:ss",
    "MM-DDTHH:mm",
    "MM-DDTHH",
    "DD",
    "DDThh:mm:ss A",
    "DDThh:mm:ssA",
    "DDThh:mm A",
    "DDThh:mmA",
    "DDThh A",
    "DDThhA",
    "DDTHH:mm:ss",
    "DDTHH:mm",
    "DDTHH",
    "ddd",
    "dddThh:mm:ss A",
    "dddThh:mm:ssA",
    "dddThh:mm A",
    "dddThh:mmA",
    "dddThh A",
    "dddThhA",
    "dddTHH:mm:ss",
    "dddTHH:mm",
    "dddTHH",
    "dddd",
    "ddddThh:mm:ss A",
    "ddddThh:mm:ssA",
    "ddddThh:mm A",
    "ddddThh:mmA",
    "ddddThh A",
    "ddddThhA",
    "ddddTHH:mm:ss",
    "ddddTHH:mm",
    "ddddTHH",
    "hh:mm:ss A",
    "hh:mm:ssA",
    "hh:mm A",
    "hh:mmA",
    "hh A",
    "hhA",
    "HH:mm:ss",
    "HH:mm",
    "HH"
  ];

  const res = moment(str, validFormats);
  if (!res.isValid()) {
    return undefined;
  }
  if (res.valueOf() < _.now() && !str.match(/[0-9]|\s/i)) {
    return res.add({ days: 7 }).valueOf();
  }
  return res.valueOf();
};

module.exports.splitDuration = (milli, components) => {
  let neg = false;
  if (milli < 0) {
    milli *= -1;
    neg = true;
  }
  if (components.years !== undefined) {
    components.years = Math.floor(milli / 3.154e10);
    milli -= components.years * 3.154e10;
    if (neg) components.years *= -1;
  }
  if (components.months !== undefined) {
    components.months = Math.floor(milli / 2.628e9);
    milli -= components.months * 2.628e9;
    if (neg) components.months *= -1;
  }
  if (components.weeks !== undefined) {
    components.weeks = Math.floor(milli / 6.0488e8);
    milli -= components.weeks * 6.048e8;
    if (neg) components.weeks *= -1;
  }
  if (components.days !== undefined) {
    components.days = Math.floor(milli / 8.64e7);
    milli -= components.days * 8.64e7;
    if (neg) components.days *= -1;
  }
  if (components.hours !== undefined) {
    components.hours = Math.floor(milli / 3.6e6);
    milli -= components.hours * 3.6e6;
    if (neg) components.hours *= -1;
  }
  if (components.minutes !== undefined) {
    components.minutes = Math.floor(milli / 6e4);
    milli -= components.minutes * 6e4;
    if (neg) components.minutes *= -1;
  }
  if (components.seconds !== undefined) {
    components.seconds = Math.floor(milli / 1e3);
    milli -= components.seconds * 1e3;
    if (neg) components.seconds *= -1;
  }
  if (components.milli !== undefined) components.milli = milli * (neg ? -1 : 1);
  return components;
};
module.exports.formatDuration = (durration, fmt) => {
  let components = {};
  if (fmt.includes("Y")) components.years = 0;
  if (fmt.includes("M")) components.months = 0;
  if (fmt.includes("W")) components.weeks = 0;
  if (fmt.includes("D")) components.days = 0;
  if (fmt.includes("H")) components.hours = 0;
  if (fmt.includes("m")) components.minutes = 0;
  if (fmt.includes("s")) components.seconds = 0;
  if (fmt.includes("S")) components.milli = 0;
  components = this.splitDuration(durration, components);
  if (components.years !== undefined) {
    fmt = fmt.replace("YYYY", components.years.toString().padStart(4, "0"));
    fmt = fmt.replace(
      "YY",
      components.years
        .toString()
        .slice(2)
        .padStart(2, "0")
    );
    fmt = fmt.replace("Y", components.years.toString());
  }
  if (components.months !== undefined) {
    fmt = fmt.replace("MM", components.months.toString().padStart(2, "0"));
    fmt = fmt.replace("M", components.months.toString());
  }
  if (components.weeks !== undefined) {
    fmt = fmt.replace("WW", components.weeks.toString().padStart(2, "0"));
    fmt = fmt.replace("W", components.weeks.toString());
  }
  if (components.days !== undefined) {
    fmt = fmt.replace("DD", components.days.toString().padStart(2, "0"));
    fmt = fmt.replace("D", components.days.toString());
  }
  if (components.hours !== undefined) {
    fmt = fmt.replace("HH", components.hours.toString().padStart(2, "0"));
    fmt = fmt.replace("H", components.hours.toString());
  }
  if (components.minutes !== undefined) {
    fmt = fmt.replace("mm", components.minutes.toString().padStart(2, "0"));
    fmt = fmt.replace("m", components.minutes.toString());
  }
  if (components.seconds !== undefined) {
    fmt = fmt.replace("ss", components.seconds.toString().padStart(2, "0"));
    fmt = fmt.replace("s", components.seconds.toString());
  }
  if (components.milli !== undefined) {
    fmt = fmt.replace("SSS", components.milli.toString().padStart(3, "0"));
    fmt = fmt.replace("S", components.milli.toString());
  }
  return fmt;
};
module.exports.getDurationMax = durration => {
  components = this.splitDuration(durration, {
    years: 0,
    months: 0,
    weeks: 0,
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    milli: 0
  });
  if (components.years !== 0) return components.years.toString() + "Y";
  else if (components.months !== 0) return components.months.toString() + "M";
  else if (components.weeks !== 0) return components.weeks.toString() + "W";
  else if (components.days !== 0) return components.days.toString() + "D";
  else if (components.hours !== 0) return components.hours.toString() + "H";
  else if (components.minutes !== 0) return components.minutes.toString() + "m";
  else if (components.seconds !== 0) return components.seconds.toString() + "s";
  else if (components.milli !== 0) return components.milli.toString() + "S";
};
module.exports.formatDate = (a, fmt) => {
  return moment(a).format(fmt);
};
module.exports.formatInterval = (a, b) => {
  const ma = moment(a);
  const mb = moment(b);
  let msg = ma.format("YYYY-MM-DD HH:mm") + " - ";
  if (mb.diff(ma, "days") !== 0) msg += mb.format("YYYY-MM-DD HH:mm");
  else msg += mb.format("HH:mm");
  msg += " [" + this.formatDuration(b - a, "HH:mm") + "]";
  return msg;
};
