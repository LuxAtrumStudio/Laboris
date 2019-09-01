const _ = require("lodash");
const inquirer = require("inquirer");
const chalk = require("chalk");

const { printHelp } = require("./util.js");

const promptConfig = config =>
  inquirer
    .prompt([
      {
        type: "input",
        name: "host",
        message: "Host URL",
        default: config.get("host")
      },
      {
        type: "password",
        name: "token",
        mask: "*",
        message: "User Token",
        default: config.get("token")
      },
      {
        type: "number",
        name: "urgency.age",
        message: "Urgency due to age",
        default: config.get("urgency.age") || 0.01429
      },
      {
        type: "number",
        name: "urgency.due",
        message: "Urgency due to due date",
        default: config.get("urgency.due") || 9.0
      },
      {
        type: "number",
        name: "urgency.parents",
        message: "Urgency due to number of parent tasks",
        default: config.get("urgency.parents") || 1.0
      },
      {
        type: "number",
        name: "urgency.children",
        message: "Urgency due to number of child tasks",
        default: config.get("urgency.children") || 0.5
      },
      {
        type: "number",
        name: "urgency.tags",
        message: "Urgency due to number of tags",
        default: config.get("urgency.tags") || 0.2
      },
      {
        type: "number",
        name: "urgency.priority",
        message: "Urgency related to the priority",
        default: config.get("urgency.priority") || -2
      },
      {
        type: "number",
        name: "urgency.active",
        message: "Urgency increase if task is active",
        default: config.get("urgency.active") || 4.0
      }
    ])
    .then(settings => {
      config.set(settings);
      console.log(chalk.cyan.bold("Set config variables"));
    });

const setOrPrint = (args, config, path = "") => {
  for (var key in args) {
    if (args[key] === true)
      console.log(
        chalk.bold(path + key + ": ") + JSON.stringify(config.get(path + key))
      );
    else if (_.isPlainObject(args[key])) {
      setOrPrint(args[key], config, path + key + ".");
    } else {
      config.set(path + key, args[key]);
      console.log(chalk.cyan.bold("Set config variable " + path + key));
    }
  }
};

module.exports = (args, config) => {
  if (args.help === true || args.h === true) {
    printHelp(
      "config [OPTIONS] [--host [URL]] [--token [TOKEN]] [--listFormat [FMT]]",
      "Set configuration values, if no arguments are specified. Then an interactive prompt is used",
      {
        "-h,--help": "displays this help text",
        "-d,--delete": "deletes all config variables",
        "--host URL": "URL for remote host server",
        "--token TOKEN": "user token for remote server",
        "--listFormat FMT": "format for the list report"
      }
    );
  } else if (args.delete === true || args.d === true) {
    config.all = {};
    console.log(chalk.cyan.bold("  Removed all saved config variables"));
  } else if (_.size(args) === 1 && args._.length === 1) {
    promptConfig(config);
  } else if (args._.length !== 1) {
    console.error(
      chalk.red(
        "  Unrecognized option in arguments '" +
          _.join(args._.slice(1), " ") +
          "'"
      )
    );
  } else {
    delete args._;
    setOrPrint(args, config);
  }
};
