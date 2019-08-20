var _ = require("lodash");
const inquirer = require("inquirer");
const chalk = require("chalk");

const { printHelp } = require("./util.js");

const promptConfig = config =>
  inquirer
    .prompt([
      {
        type: "input",
        name: "host",
        default: config.get("host")
      },
      {
        type: "password",
        name: "token",
        mask: "*",
        default: config.get("token")
      }
    ])
    .then(settings => {
      config.set(settings);
      console.log(chalk.cyan.bold("Set config variables"));
    });

module.exports.cmd = (args, config) => {
  if (args.help === true || args.h === true) {
    printHelp(
      "config [OPTIONS] [--host URL] [--token TOKEN]",
      "Set configuration values, if no arguments are specified. Then an interactive prompt is used",
      {
        "-h,--help": "displays this help text",
        "-d,--delete": "deletes all config variables",
        "--host URL": "URL for remote host server",
        "--token TOKEN": "user token for remote server"
      }
    );
  } else if (args.delete === true || args.d === true) {
    config.all = {};
    console.log(chalk.cyan.bold("Removed all saved config variables"));
  } else if (_.size(args) === 1 && args._.length === 1) {
    promptConfig(config);
  } else if (args._.length !== 1) {
    console.error(
      chalk.red(
        "Unrecognized option in arguments '" +
          _.join(args._.slice(1), " ") +
          "'"
      )
    );
  } else {
    delete args._;
    config.set(args);
    console.log(chalk.cyan.bold("Set config variables"));
  }
};
