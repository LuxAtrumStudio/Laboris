const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, error } = require("../graphql.js");
const { parseDate } = require("../common.js");
const { short } = require("../print.js");
const { printHelp, getTask } = require("../util.js");

module.exports = (args, config) => {
  args._ = args._.slice(1);
  if (args.help === true || args.h === true) {
    printHelp(
      "start TASK [TIME]",
      "Start a timer for the specified task. If no TIME value is provided, then the current time is used.",
      {
        "-h,--help": "displays this help text",
        TASK: "task identification, either id or title",
        TIME: "datetime or time reference for the start time of the task"
      }
    );
    return;
  }
  if (args._.length === 0) {
    console.log(chalk.red.bold("  Must specify a task"));
  } else {
    if (_.last(args._).match(/\+|[0-9]/)) args._ = args._.slice(0, -1);
    getTask(_.join(args._, " "), config, data => {
      if (_.last(args.__).match(/[\+-]|[0-9]/)) {
        console.log(_.last(args.__));
        console.log(new Date(parseDate(_.last(args.__))));
      }
    });
  }
};
