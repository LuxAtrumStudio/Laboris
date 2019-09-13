const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
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
  } else if (args._.length === 0) {
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
      var startTime = _.now();
      if (
        /^((\+|-)[0-9]*[whms]?)|(([0-9]|[-/:T]|am|pm)+)$/i.test(_.last(args.__))
      ) {
        startTime = parseDate(_.last(args.__));
      }
      mutation(`start(id:\"${id}\", startTime: ${startTime}){id,title}`, config)
        .then(data => {
          console.log(
            chalk.green.bold(
              `  Started ${data.start.id.slice(0, 4)} ${
                data.start.title
              } ${new Date(startTime).toLocaleTimeString()} [00:00]`
            )
          );
        })
        .catch(errors);
    });
  }
};
