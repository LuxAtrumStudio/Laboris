const _ = require("lodash");
const inquirer = require("inquirer");
const chalk = require("chalk");
const fuzzy = require("fuzzy");

const { printHelp, parseDate } = require("./util.js");
const { get, post } = require("./remote.js");
const { short } = require("./print.js");

const cmdAdd = (args, config) => {
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
    cmdAdd(
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
