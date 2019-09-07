const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
const { printHelp, getTask, extract } = require("../util.js");
const { short } = require("../print.js");

module.exports = (args, config) => {
  args._ = args._.slice(1);
  if (args.help === true || args.h === true) {
    printHelp(
      "modify TASK [OPTIONS] [TITLE...]",
      "Modifies an existing task, to use the new options and title. If no options or title are specified, then an interactive prompt is used.",
      {
        "-h,--help": "displays this help text",
        "-p,--priority": "task priority (0-5)[5]",
        "--due,--dueDate": "task due date",
        "--parent,--parents": "list of parent tasks",
        "--child,--children": "list of child tasks",
        "-t,--tag,--tags": "list of task tags",
        TASK: "Single word specifier for task, either the title or the id",
        TITLE:
          "Title and string specifier for task. Any word starting with '+' is considered a parent. Any word starting with '_' is considered a child. Any word starting with '@' is considered a tag. The priority can be specified with p:#, and the due date can be specified with due:DUEDATE. Any words that do not meet one of these previous specifications is considered to be part of the tasks title"
      }
    );
  } else if (args._.length === 0) {
    console.log(chalk.red.bold("  Must specify a task to modify"));
  } else {
    getTask(args._[0], config, id => {
      args._ = args._.slice(1);
      var opts = {
        title: extract.title(args, null),
        priority: extract.priority(args, null),
        dueDate: extract.dueDate(args, null),
        parents: extract.parents(args, null),
        children: extract.children(args, null),
        tags: extract.tags(args, null),
        hidden: args.hidden || null
      };
      if (!_.some(opts, v => v !== null)) {
        console.log(chalk.yellow.bold("  No options will be updated"));
        console.log(chalk.yellow("    Interactive prompt is a WIP"));
      } else {
        Object.keys(opts).forEach(key => opts[key] == null && delete opts[key]);
        var mutationString = `modifyTask(id:"${id}"`;
        for (const key in opts) {
          if (typeof opts[key] === "object")
            mutationString += "," + key + ":" + JSON.stringify(opts[key]);
          else mutationString += "," + key + ":" + opts[key];
        }
        mutationString +=
          "){id,title,parents{title},children{title},tags,dueDate,urg}";
        mutation(mutationString, config)
          .then(data => {
            console.log(chalk.blue.bold(`Modified task "${id}":`));
            console.log(short(data.modifyTask));
          })
          .catch(errors);
      }
    });
  }
};
