const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
const { getTask, prompt, connectionError } = require("../util.js");
const { short } = require("../print.js");

module.exports = (args, config) => {
  getTask(_.join(args._.slice(1), " "), config, id => {
    query(`get(id:\"${id}\"){id,title,parents{title},tags,dueDate,urg}`, config)
      .then(data => {
        prompt({
          confirm: {
            type: "confirm",
            message: chalk.red.bold("Delete") + short(data.get),
            default: false
          }
        }).then(opts => {
          if (opts.confirm)
            mutation(`delete(id:"${data.get.id}")`, config)
              .then(res => {
                console.log(chalk.red.bold("Deleted task:", res.delete));
              })
              .catch(errors);
        });
      })
      .catch(errors);
  });
};
