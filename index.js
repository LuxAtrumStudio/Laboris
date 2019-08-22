const ConfigStore = require("configstore");
const chalk = require("chalk");
const args = require("minimist")(process.argv.slice(2));

const package = require("./package.json");

var config = new ConfigStore(
  "laboris",
  {
    urgency: {
      age: 0.01429,
      due: 9.0,
      parents: 1.0,
      children: 0.5,
      tags: 0.2,
      priority: -2.0,
      active: 4.0
    },
    listFormat:
      "{id:4-} {p} {dueDelta:>} {title:<20+} {parents} {tags} {urg:.3f}"
  },
  { globalConfigPath: true }
);

const { urgColor } = require("./print.js");

console.log(args);

if (args._[0] === "add") require("./action.js").add(args, config);
else if (args._[0] === "start") require("./action.js").start(args, config);
else if (args._[0] === "stop") require("./action.js").stop(args, config);
else if (args._[0] === "modify") console.log(chalk.blue.bold("MODIFY"));
else if (args._[0] === "done") console.log(chalk.green.bold("DONE"));
else if (args._[0] === "sync") console.log(chalk.magenta.bold("SYNC"));
else if (args._[0] === "config") require("./config.js").cmd(args, config);
else if (args._.length === 0 && args._.help === true) console.log("HELP");
else require("./reports.js").list(args, config);
