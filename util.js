const _ = require("lodash");
const chalk = require("chalk");
const moment = require("moment");
const inquirer = require("inquirer");
const fuzzy = require("fuzzy");
const { parseDate } = require("./common.js");
const { query, mutation, errors } = require("./graphql.js");
const { short } = require("./print.js");
const { wrap } = require("./fmt.js");

inquirer.registerPrompt(
  "autocomplete",
  require("inquirer-autocomplete-prompt")
);
inquirer.registerPrompt(
  "checkbox-plus",
  require("inquirer-checkbox-plus-prompt")
);

module.exports.printHelp = (usage, description, args) => {
  console.log("laboris " + usage);

  if (description) {
    console.log("\n" + wrap(description, 2, true, 78) + "\n");
  }

  const keyLength = _.maxBy(Object.keys(args), k => k.length).length;
  for (const key in args) {
    help = wrap(args[key], keyLength + 4, false);
    console.log("  " + key.padEnd(keyLength) + "  " + help);
  }
};

module.exports.prompt = options => {
  var prompts = [];
  for (const key in options) {
    prompt = {
      name: key
    };
    if (!options[key].message) prompt.message = _.startCase(key);
    else prompt.message = options[key].message;
    if (!options[key].type && options[key].choices) {
      if (options[key].multiple) {
        prompt.type = "checkbox-plus";
        prompt.searchable = true;
      } else prompt.type = "autocomplete";
      if (options[key].only === false) {
        prompt.suggestOnly = true;
        prompt.source = (_, input) => {
          input = input || "";
          return new Promise(resolve =>
            resolve(
              fuzzy
                .filter(input, options[key].choices.concat(input))
                .map(el => el.original)
            )
          );
        };
      } else {
        prompt.source = (_, input) => {
          input = input || "";
          return new Promise(resolve =>
            resolve(
              fuzzy.filter(input, options[key].choices).map(el => el.original)
            )
          );
        };
      }
    } else if (!options[key].type) prompt.type = "input";
    else prompt.type = options[key].type;
    if (options[key].default !== undefined)
      prompt.default = options[key].default;
    if (options[key].validator) prompt.validate = options[key].validator;
    prompts.push(prompt);
  }
  return inquirer.prompt(prompts);
};

module.exports.getTask = (queryStr, config, callback) => {
  query(
    `find(query:${JSON.stringify(
      queryStr
    )}){id,title,parents{title},children{title},tags,dueDate,urg}`,
    config
  )
    .then(data => {
      if (data.find.length === 0) callback([]);
      else if (data.find.length === 1) callback(data.find[0].id);
      else {
        const choices = {};
        data.find.forEach(o => {
          choices[short(o)] = o.id;
        });
        const keys = Object.keys(choices);
        inquirer
          .prompt([
            {
              type: "autocomplete",
              name: "task",
              message: "Specify task",
              source: (_, input) => {
                input = input || "";
                return new Promise(resolve =>
                  resolve(fuzzy.filter(input, keys).map(el => el.original))
                );
              }
            }
          ])
          .then(data => {
            callback(choices[data.task]);
          });
      }
    })
    .catch(errors);
};

module.exports.extract = {};

module.exports.extract.title = (args, defaultVal = "") => {
  const res = _.join(
    _.filter(
      args._,
      arg =>
        !(
          _.startsWith(arg, "@") ||
          _.startsWith(arg, "+") ||
          _.startsWith(arg, "_") ||
          _.startsWith(arg, "p:") ||
          _.startsWith(arg, "due:")
        )
    ),
    " "
  );
  if (res !== "") return res;
  return defaultVal;
};

module.exports.extract.priority = (args, defaultVal = 5) => {
  if (args.p) return parseInt(args.p);
  else if (args.priority) return parseInt(args.priority);
  else if (_.find(args._, arg => _.startsWith(arg, "p:")))
    return parseInt(_.find(args._, arg => _.startsWith(arg, "p:")).slice(2));
  else return defaultVal;
};

module.exports.extract.dueDate = (args, defaultVal = undefined) => {
  if (args.due) return parseDate(args.due);
  else if (args.dueDate) return parseDate(args.dueDate);
  else if (_.find(args._, arg => _.startsWith(arg, "due:")))
    return parseDate(_.find(args._, arg => _.startsWith(arg, "due:")).slice(4));
  else return defaultVal;
};

module.exports.extract.parents = (args, defaultVal = []) => {
  const res = _.filter(
    _.concat(
      args.parents,
      args.parent,
      _.map(_.filter(args._, arg => _.startsWith(arg, "+")), o => o.slice(1))
    ),
    o => o !== undefined
  );
  if (res.length !== 0) return res;
  return defaultVal;
};

module.exports.extract.children = (args, defaultVal = []) => {
  const res = _.filter(
    _.concat(
      args.children,
      args.child,
      _.map(_.filter(args._, arg => _.startsWith(arg, "_")), o => o.slice(1))
    ),
    o => o !== undefined
  );
  if (res.length !== 0) return res;
  return defaultVal;
};

module.exports.extract.tags = (args, defaultVal = []) => {
  const res = _.filter(
    _.concat(
      args.tags,
      args.tag,
      args.t,
      _.map(_.filter(args._, arg => _.startsWith(arg, "@")), o => o.slice(1))
    ),
    o => o !== undefined
  );
  if (res.length !== 0) return res;
  return defaultVal;
};
