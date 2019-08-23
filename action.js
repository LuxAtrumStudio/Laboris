const _ = require("lodash");
const inquirer = require("inquirer");
const chalk = require("chalk");
const fuzzy = require("fuzzy");
const moment = require("moment");

const { printHelp, parseDate } = require("./util.js");
const { get, post } = require("./remote.js");
const { duration, refName, short } = require("./print.js");

const actionAdd = (args, config) => {
  if (args.title.length === 0) {
    console.log(chalk.red.bold("Task must have a title"));
    return;
  } else {
    args.title = _.join(args.title, " ");
  }
  if (args.dueDate) {
    const src = args.dueDate.slice(4);
    args.dueDate = parseDate(src);
    if (!args.dueDate) {
      console.log(
        chalk.red.bold(
          'Invalid date format "' + src + '" view help for valid formats.'
        )
      );
      return;
    }
  }
  if (args.priority) {
    args.priority = _.toSafeInteger(args.priority.slice(2));
  }
  console.log(chalk.blue.bold("Created new task"));
  post("/", args, config)
    .then(res => {
      console.log(short(res, config));
    })
    .catch(err => {
      console.log(err);
      console.log(
        chalk.yellow.bold("Network issue, try to sync new tasks later")
      );
    });
};

const promptAdd = config => {
  get("/reference", config).then(ref => {
    const tags = _.uniq(_.flattenDeep(_.map(ref, "tags")));
    const titles = _.uniq(_.flattenDeep(_.map(ref, "title")));
    inquirer.registerPrompt(
      "autocomplete",
      require("inquirer-autocomplete-prompt")
    );
    inquirer
      .prompt([
        {
          type: "input",
          name: "title",
          message: "Title",
          validate: input => input.length !== 0
        },
        {
          type: "input",
          name: "due",
          message: "Due Date"
        },
        {
          type: "number",
          name: "priority",
          message: "Priority",
          default: 5,
          validate: input => input >= 0 && input <= 5
        },
        {
          type: "autocomplete",
          name: "tags",
          message: "Tag",
          source: (answers, input) => {
            input = input || "";
            return new Promise(resolve => {
              resolve(fuzzy.filter(input, tags).map(el => el.original));
            });
          },
          suggestOnly: true
        },
        {
          type: "autocomplete",
          name: "parents",
          message: "Parent",
          source: (answers, input) => {
            input = input || "";
            return new Promise(resolve => {
              resolve(fuzzy.filter(input, titles).map(el => el.original));
            });
          },
          suggestOnly: true,
          validate: input =>
            input.length === 0 || _.indexOf(titles, input) !== -1
        }
      ])
      .then(res => {
        console.log(res);
      });
  });
};

module.exports.add = (args, config) => {
  if (args.help === true || args.h === true) {
    printHelp(
      "add TITLE",
      "Add a new task to the database for your user. If the necessary arguments are not proviced, then an interactive prompt is used to request them.",
      {
        "-h,--help": "displays this help text"
      }
    );
  } else if (args._.length === 1) {
    promptAdd(config);
  } else {
    actionAdd(
      {
        title: _.reject(
          args._,
          o =>
            o[0] === "@" ||
            o[0] === "+" ||
            _.startsWith(o, "due:") ||
            _.startsWith(o, "p:")
        ).slice(1),
        tags: args.tags
          ? args.tags
          : _.map(_.filter(args._, o => o[0] === "@"), el => el.slice(1)),
        parents: args.parents
          ? args.parents
          : _.map(_.filter(args._, o => o[0] === "+"), el => el.slice(1)),
        dueDate: args.due
          ? args.due
          : _.find(args._, o => _.startsWith(o, "due:")),
        priority: args.pri
          ? args.pri
          : _.find(args._, o => _.startsWith(o, "p:")) || "p:5"
      },
      config
    );
  }
};

const startAction = (task, time, config) => {
  post("/start/" + task._id, {}, config)
    .then(res => {
      if (res.error) console.log(chalk.yellow.bold("  " + res.error));
      else
        console.log(
          chalk.yellow.bold(
            "  Starting " +
              task.title +
              " " +
              moment(time).format("LT") +
              " (00:00)"
          )
        );
    })
    .catch(err => {
      console.log(
        chalk.yellow.bold(
          "Network issue, task will start when connection is reestablished"
        )
      );
    });
};

module.exports.start = (args, config) => {
  if (args.help === true || args.h === true) {
    printHelp("start TASK [TIME]", "Start work timer for a specified task", {
      "-h,--help": "displays this help text",
      TASK: "reference for a task (id/title)",
      TIME: "time/time delta to start the timer"
    });
  }
  get("/find?query=" + args._[1], config)
    .then(res => {
      if (res.length === 0)
        console.log(
          chalk.yellow.bold(
            '  Could not find task matching "' + args._[1] + '"'
          )
        );
      else if (res.length > 1)
        inquirer
          .prompt([
            {
              type: "list",
              name: "task",
              message: "Multiple matching tasks",
              choices: _.map(res, o => refName(o))
            }
          ])
          .then(choice =>
            startAction(
              _.find(res, o => o._id.startsWith(choice.task.split(" ")[0])),
              parseDate(args._[2]) || Date.now(),
              config
            )
          );
      else startAction(res[0], parseDate(args._[2]) || Date.now(), config);
    })
    .catch(err => {
      console.log(err);
    });
};

const stopAction = (task, time, config) => {
  if (task)
    post("/stop/" + task._id, {}, config)
      .then(res => {
        console.log(res);
        if (res.error) console.log(chalk.yellow.bold("  " + res.error));
        else
          console.log(
            chalk.yellow.bold(
              "  Stoping " +
                task.title +
                " " +
                moment(time).format("LT") +
                " (" +
                duration(_.last(res.times)[0], _.last(res.times)[1]) +
                ")"
            )
          );
      })
      .catch(err => {
        console.log(err);
        console.log(
          chalk.yellow.bold(
            "Network issue, task will stop when connection is reestablished"
          )
        );
      });
  else
    post("/stop/", {}, config)
      .then(res => {
        if (res.error) console.log(chalk.yellow.bold("  " + res.error));
        else
          res.forEach(el => {
            console.log(
              chalk.yellow.bold(
                "  Stoping " +
                  el.title +
                  " " +
                  moment(time).format("LT") +
                  " (" +
                  duration(_.last(el.times)[0], _.last(el.times)[1]) +
                  ")"
              )
            );
          });
      })
      .catch(err => {
        console.log(
          chalk.yellow.bold(
            "Network issue, all tasks will stop when connection is reestablished"
          )
        );
      });
};

module.exports.stop = (args, config) => {
  if (args.help === true || args.h === true) {
    printHelp(
      "stop [TASK] [TIME]",
      "Stop work timer for a specified task. If no task is specified, then all active tasks are stoped.",
      {
        "-h,--help": "displays this help text",
        TASK: "reference for a task (id/title)",
        TIME: "time/time delta to start the timer"
      }
    );
  }
  if (args._[1])
    get("/find?query=" + args._[1], config)
      .then(res => {
        if (res.length === 0)
          console.log(
            chalk.yellow.bold(
              '  Could not find task matching "' + args._[1] + '"'
            )
          );
        else if (res.length > 1)
          inquirer
            .prompt([
              {
                type: "list",
                name: "task",
                message: "Multiple matching tasks",
                choices: _.map(res, o => refName(o))
              }
            ])
            .then(choice =>
              stopAction(
                _.find(res, o => o._id.startsWith(choice.task.split(" ")[0])),
                parseDate(args._[2]) || Date.now(),
                config
              )
            );
        else stopAction(res[0], parseDate(args._[2]) || Date.now(), config);
      })
      .catch(err => {
        console.log(err);
      });
  else stopAction(undefined, Date.now(), config);
};
