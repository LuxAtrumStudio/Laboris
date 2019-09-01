const _ = require("lodash");
const chalk = require("chalk");
const { query, mutation, error } = require("../graphql.js");
const { prompt, connectionError, extract } = require("../util.js");
const { parseDate } = require("../common.js");
const { short } = require("../print.js");

module.exports = (args, config) => {
  args._ = args._.slice(1);
  if (args._.length === 0 || args.i === true) {
    query("open{id,title,tags}", config)
      .then(data => {
        const titles = _.map(data.open, "title");
        const tags = _.flatten(_.map(data.open, "tags"));
        prompt({
          title: {
            default: extract.title(args),
            validator: input => input.length !== 0
          },
          priority: {
            type: "number",
            default: extract.priority(args)
          },
          dueDate: {
            default: extract.dueDate(args),
            validator: input => parseDate(input) !== undefined || input === ""
          },
          parents: {
            multiple: true,
            choices: titles,
            default: extract.parents(args)
          },
          children: {
            multiple: true,
            choices: titles,
            default: extract.children(args)
          },
          tags: {
            multiple: true,
            choices: _.uniq(_.concat(tags, extract.tags(args))),
            only: false,
            default: extract.tags(args)
          },
          hidden: {
            type: "confirm",
            default: false
          }
        }).then(opts => {
          mutation(
            `newTask(title:"${opts.title}",priority:${opts.priority},dueDate:${
              opts.dueDate !== "" ? parseDate(opts.dueDate) : null
            },parents:${JSON.stringify(opts.parents)},children:${JSON.stringify(
              opts.children
            )},tags:${JSON.stringify(opts.tags)},hidden:${JSON.stringify(
              opts.hidden
            )}){id,title,parents{title},children{title},tags,dueDate,urg}`,
            config
          )
            .then(res => {
              console.log(short(res.newTask));
            })
            .catch(error);
        });
      })
      .catch(error);
  } else {
    const opts = {
      title: extract.title(args),
      priority: extract.priority(args),
      dueDate: extract.dueDate(args),
      parents: extract.parents(args),
      children: extract.children(args),
      tags: extract.tags(args),
      hidden: args.hidden || false
    };
    mutation(
      `newTask(title:"${opts.title}",priority:${
        opts.priority
      },dueDate:${parseDate(opts.dueDate) || null},parents:${JSON.stringify(
        opts.parents
      )},children:${JSON.stringify(opts.children)},tags:${JSON.stringify(
        opts.tags
      )},hidden:${JSON.stringify(
        opts.hidden
      )}){id,title,parents{title},children{title},tags,dueDate,urg}`,
      config
    )
      .then(res => {
        console.log(chalk.blue.bold("Created new task:"));
        console.log(short(res.newTask));
      })
      .catch(error);
  }
};
