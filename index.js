const ConfigStore = require("configstore");
const chalk = require("chalk");
const args = require("minimist")(process.argv.slice(2));

const package = require("./package.json");

var config = new ConfigStore("laboris", {}, { globalConfigPath: true });

const { urgColor } = require("./print.js");

console.log(args);

if (args._[0] === "add") require("./action.js").add(args, config);
else if (args._[0] === "start") console.log(chalk.yellow.bold("START"));
else if (args._[0] === "stop") console.log(chalk.yellow.bold("STOP"));
else if (args._[0] === "modify") console.log(chalk.blue.bold("MODIFY"));
else if (args._[0] === "done") console.log(chalk.green.bold("DONE"));
else if (args._[0] === "sync") console.log(chalk.magenta.bold("SYNC"));
else if (args._[0] === "config") require("./config.js").cmd(args, config);
else if (args._.length === 0 && args._.help === true) console.log("HELP");
else console.log(chalk.bold("LIST"));
