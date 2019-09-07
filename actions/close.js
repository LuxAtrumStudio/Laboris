const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
const { printHelp, getTask, extract } = require("../util.js");
const { short } = require("../print.js");

module.exports = (args, config) => {
  args._ = args._.slice(1);
  if (args.help === true || args.h === true) {
    printHelp(
      "close TASK",
      "Moves a currently open task to the list of closed tasks",
      {
        "-h,--help": "displays this help text",
        TASK: "task identification, either id or title"
      }
    );
  } else if (args._.length === 0) {
    console.log(chalk.red.bold("  Must specify a task to close"));
  } else {
    getTask(args._[0], config, id => {
      args._ = args._.slice(1);
      mutation(
        `close(id:"${id}"){id,title,parents{title},children{title},tags,dueDate,urg}`,
        config
      )
        .then(data => {
          console.log(chalk.green.bold(`Closed task "${id}":`));
          console.log(short(data.close));
        })
        .catch(errors);
    });
  }
};
