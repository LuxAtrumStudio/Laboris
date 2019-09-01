const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
const { getTask, prompt, connectionError } = require("../util.js");
const { short } = require("../print.js");

module.exports = (args, config) => {
  getTask(_.join(args._.slice(1), " "), config, id => {
    prompt({
      confirm: {
        type: "confirm",
        message: chalk.red.bold("Delete") + short(data[0]),
        default: false
      }
    }).then(opts => {
      if (opts.confirm)
        mutation(`delete(id:"${data[0].id}")`, config)
          .then(res => {
            console.log(chalk.red.bold("Deleted task:", res.delete));
          })
          .catch(errors);
    });
  });
};
