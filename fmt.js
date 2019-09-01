const _ = require("lodash");

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

module.exports.parseFormat = fmt => {
  const re = /{([^:]+)(:([<^>])?(\d+)?(\.(\d+))?([-\+])?([sdf])?)?}/;
  return (specifier = _.map(fmt.split(" "), el => {
    const match = re.exec(el);
    return {
      key: match[1],
      width: parseInt(match[4]),
      precision: parseInt(match[6]),
      align: match[3],
      wrap: match[7],
      type: match[8]
    };
  }));
};

module.exports.fmtData = (fmt, data) => {
  data = data[fmt.key];
  if (data === undefined) return "";
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
