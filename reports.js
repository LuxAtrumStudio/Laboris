const _ = require("lodash");
const chalk = require("chalk");

const { urg, fmt } = require("./util.js");
const { get } = require("./remote.js");
const {
  urgColor,
  dateDeltaMajor,
  dateDeltaFull,
  dateDeltaMin
} = require("./print.js");

module.exports.list = (args, config) => {
  const re = /{([^:]+)(:([<^>])?(\d+)?(\.(\d+))?([-\+])?([sdf])?)?}/;
  const specifier = _.map(config.get("listFormat").split(" "), el => {
    const match = re.exec(el);
    return {
      key: match[1],
      width: parseInt(match[4]),
      precision: parseInt(match[6]),
      align: match[3],
      wrap: match[7],
      type: match[8]
    };
  });
  console.log(specifier);
  get("/", config)
    .then(res => {
      res = _.sortBy(
        _.map(res, el => {
          return {
            ...el,
            id: el._id,
            p: el.priority,
            tags: _.join(el.tags, " "),
            parents: _.join(el.parents, " "),
            urg: urg(el, config),
            dueDelta: dateDeltaMajor(Date.now(), el.dueDate)
          };
        }),
        el => -el.urg
      );
      var table = {};
      for (var id in specifier) {
        table[specifier[id].key] = _.map(res, el => fmt(specifier[id], el));
        table[specifier[id].key] = _.map(table[specifier[id].key], el => {
          const maxLength = _.maxBy(table[specifier[id].key], s => s.length)
            .length;
          if (!specifier[id].width) {
            if (specifier[id].align === "<")
              return el + " ".repeat(maxLength - el.length);
            else if (specifier[id].align === "^")
              return (
                " ".repeat(Math.ceil((maxLength - el.length) / 2.0)) +
                el +
                " ".repeat(Math.floor((maxLength - el.length) / 2.0))
              );
            else return " ".repeat(maxLength - el.length) + el;
          }
          return el;
        });
      }

      for (var id in res) {
        var str = "";
        for (var idx in specifier) {
          str += "  " + table[specifier[idx].key][id];
        }
        str = str.slice(2);
        if (id % 2 === 0) console.log(urgColor(res[id].urg)(str));
        else console.log(chalk.bgBlack(urgColor(res[id].urg)(str)));
      }
    })
    .catch(err => {
      console.log(err);
      console.log(chalk.yellow.bold("Network issue, failed to retrieve tasks"));
    });
};
