const ConfigStore = require("configstore");
const chalk = require("chalk");
var args = require("minimist")(process.argv.slice(2));
args.__ = process.argv.slice(2);

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

console.log(args);

if (args._[0] === "add") require("./actions/create.js")(args, config);
else if (args._[0] === "delete") require("./actions/delete.js")(args, config);
else if (args._[0] === "start") require("./actions/start.js")(args, config);
else if (args._[0] === "stop") require("./actions/stop.js")(args, config);
// else if (args._[0] === "modify") console.log(chalk.blue.bold("MODIFY"));
// else if (args._[0] === "done") console.log(chalk.green.bold("DONE"));
else if (args._[0] === "config") require("./config.js")(args, config);
// else if (args._.length === 0 && args._.help === true) console.log("HELP");
else require("./reports/list.js")(args, config);
