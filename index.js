#!/usr/bin/env node
const ConfigStore = require("configstore");
const chalk = require("chalk");
const { printHelp } = require("./util.js");
var args = require("minimist")(process.argv.slice(2));
args.__ = process.argv.slice(2);

const package = require("./package.json");

const mainHelp = () => {
  printHelp("[COMMAND]", "Laboris CLI task manager", {
    COMMAND:
      "Sub command {add,modify,start,stop,delete,done,config,report} Defaults to report.list"
  });
};

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

if (args._[0] === "add" || args._[0] === "create")
  require("./actions/create.js")(args, config);
else if (args._[0] === "delete") require("./actions/delete.js")(args, config);
else if (args._[0] === "start") require("./actions/start.js")(args, config);
else if (args._[0] === "stop") require("./actions/stop.js")(args, config);
else if (args._[0] === "modify") require("./actions/modify.js")(args, config);
else if (args._[0] === "close") require("./actions/close.js")(args, config);
else if (args._[0] === "reopen") require("./actions/reopen.js")(args, config);
else if (args._[0] === "config") require("./config.js")(args, config);
else if (args._.length === 0 && (args.help === true || args.h === true))
  mainHelp();
else require("./reports/list.js")(args, config);
