const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
const { parseDate } = require("../common.js");
const { duration, short } = require("../print.js");
const { printHelp, getTask } = require("../util.js");

module.exports = (args, config) => {
  args._ = args._.slice(1);
  if (args.help === true || args.h === true) {
    printHelp(
      "stop TASK [TIME]",
      "Stop a timer for the specified task. If no TIME value is provided, then the current time is used.",
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
    if (
      args._.length > 1 &&
      _.last(args._) &&
      _.last(args._)
        .toString()
        .match(/\+|[0-9]/)
    )
      args._ = args._.slice(0, -1);
    getTask(_.join(args._, " "), config, id => {
      var stopTime = _.now();
      if (_.last(args.__).match(/[\+-]|[0-9]/)) {
        stopTime = parseDate(_.last(args.__));
      }
      mutation(
        `stop(id:\"${id}\", stopTime: ${stopTime}){id,title,times}`,
        config
      )
        .then(data => {
          const last = _.last(data.stop.times);
          console.log(
            chalk.green.bold(
              `  Stopped ${data.stop.id.slice(0, 4)} ${
                data.stop.title
              } ${new Date(stopTime).toLocaleTimeString()} [${duration(
                last[0],
                last[1]
              )}]`
            )
          );
        })
        .catch(errors);
    });
  }
};
