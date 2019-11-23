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

module.exports.error = msg => {
  console.log(chalk.red.bold(wrapStr("  ERROR: " + msg, 60, 9)));
};
module.exports.msg = msg => {
  console.log(chalk.cyan.bold(wrapStr("  " + msg, 60, 2)));
};
