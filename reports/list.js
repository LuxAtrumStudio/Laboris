const _ = require("lodash");
const moment = require("moment");
const chalk = require("chalk");
const { query, mutation, error } = require("../graphql.js");
const { extract } = require("../util.js");
const { parseFormat, fmtData } = require("../fmt.js");
const { parseDate } = require("../common.js");
const {
  dateDeltaMajor,
  dateDeltaMin,
  dateDeltaFull,
  urgColor
} = require("../print.js");

const fmtKeys = fmtStr => {
  const fmt = _.map(parseFormat(fmtStr), "key");
  var keys = ["urg", "active"];
  if (_.includes(fmt, "id")) {
    keys.push("id");
  }
  if (_.includes(fmt, "title")) {
    keys.push("title");
  }
  if (_.some(["p", "pri", "priority"], o => _.includes(fmt, o))) {
    keys.push("priority");
  }
  if (
    _.some(
      [
        "dueDate",
        "dueDelta",
        "dueDeltaMajor",
        "dueDeltaMin",
        "dueDeltaFull",
        "dueDateTime",
        "dueDateLong",
        "dueDateTimeLong"
      ],
      o => _.includes(fmt, o)
    )
  ) {
    keys.push("dueDate");
  }
  if (
    _.some(
      [
        "entryDate",
        "entryDelta",
        "entryDeltaMajor",
        "entryDeltaMin",
        "entryDeltaFull",
        "entryDateTime",
        "entryDateLong",
        "entryDateTimeLong"
      ],
      o => _.includes(fmt, o)
    )
  ) {
    keys.push("entryDate");
  }
  if (
    _.some(
      [
        "doneDate",
        "doneDelta",
        "doneDeltaMajor",
        "doneDeltaMin",
        "doneDeltaFull",
        "doneDateTime",
        "doneDateLong",
        "doneDateTimeLong"
      ],
      o => _.includes(fmt, o)
    )
  ) {
    keys.push("doneDate");
  }
  if (
    _.some(
      [
        "modifiedDate",
        "modifiedDelta",
        "modifiedDeltaMajor",
        "modifiedDeltaMin",
        "modifiedDeltaFull",
        "modifiedDateTime",
        "modifiedDateLong",
        "modifiedDateTimeLong"
      ],
      o => _.includes(fmt, o)
    )
  ) {
    keys.push("modifiedDate");
  }
  if (_.some(["parents", "parentCount"], o => _.includes(fmt, o))) {
    keys.push("parents{id,title}");
  }
  if (_.some(["children", "childCount"], o => _.includes(fmt, o))) {
    keys.push("children{id,title}");
  }
  if (_.some(["tags", "tagCount"], o => _.includes(fmt, o))) {
    keys.push("tags");
  }
  if (_.some(["hidden"], o => _.includes(fmt, o))) {
    keys.push("hidden");
  }
  return _.join(keys, ",");
};

const genDateKeys = (prefix, value) => {
  if (!value) return {};
  var res = {};
  res[prefix + "Date"] = moment(value).format("YYYY-MM-DD");
  res[prefix + "DateTime"] = moment(value).format("YYYY-MM-DD HH:mm:ss");
  res[prefix + "DateLong"] = moment(value).format("dddd, MMMM Do YYYY");
  res[prefix + "DateTimeLong"] = moment(value).format(
    "dddd, MMMM Do YYYY, h:mm:ss a"
  );
  res[prefix + "Delta"] = dateDeltaMajor(_.now(), value);
  res[prefix + "DeltaMajor"] = dateDeltaMajor(_.now(), value);
  res[prefix + "DeltaMin"] = dateDeltaMin(_.now(), value);
  res[prefix + "DeltaFull"] = dateDeltaFull(_.now(), value);
  return res;
};

const genPrintKeys = task => {
  return {
    title: task.title,
    id: task.id,
    priority: task.priority,
    parents: task.parents
      ? _.join(_.map(task.parents, "title"), " ")
      : undefined,
    parentCount: task.parents ? task.parents.length : undefined,
    children: task.children
      ? _.join(_.map(task.children, "title"), " ")
      : undefined,
    childCount: task.children ? task.children.length : undefined,
    tags: task.tags ? _.join(task.tags, " ") : undefined,
    tagCount: task.tags ? task.tags.length : undefined,
    urg: task.urg,
    hidden: task.hidden,
    active: task.active,
    ...genDateKeys("due", task.dueDate),
    ...genDateKeys("entry", task.entryDate),
    ...genDateKeys("done", task.doneDate),
    ...genDateKeys("modified", task.modifiedDate)
  };
};

module.exports = (args, config) => {
  var queryStr = "filter";
  parsedArgs = {
    priority: extract.priority(args, null),
    parents: extract.parents(args),
    children: extract.children(args),
    tags: extract.tags(args),
    dueBefore:
      extract.dueDate(args) ||
      (args.dueBefore ? parseDate(args.dueBefore) : undefined),
    dueAfter: args.dueAfter ? parseDate(args.dueAfter) : undefined,
    entryBefore: args.entryBefore ? parseDate(args.entryBefore) : undefined,
    entryAfter: args.entryAfter ? parseDate(args.entryAfter) : undefined,
    modifiedBefore: args.modifiedBefore
      ? parseDate(args.modifiedBefore)
      : undefined,
    modifiedAfter: args.modifiedAfter
      ? parseDate(args.modifiedAfter)
      : undefined,
    hidden: args.hidden || undefined
  };
  if (
    parsedArgs.priority !== null ||
    parsedArgs.parents.length !== 0 ||
    parsedArgs.children.length !== 0 ||
    parsedArgs.tags.length !== 0 ||
    parsedArgs.dueBefore !== undefined ||
    parsedArgs.dueAfter !== undefined ||
    parsedArgs.entryBefore !== undefined ||
    parsedArgs.entryAfter !== undefined ||
    parsedArgs.modifiedBefore !== undefined ||
    parsedArgs.modifiedAfter !== undefined ||
    parsedArgs.hidden !== undefined
  ) {
    queryStr += "(";
    for (const key in parsedArgs) {
      if (typeof parsedArgs[key] === "object") {
        if (parsedArgs[key] !== null && parsedArgs[key].length !== 0)
          queryStr += key + ":" + JSON.stringify(parsedArgs[key]) + ",";
      } else if (parsedArgs[key] !== null && parsedArgs[key] !== undefined) {
        queryStr += key + ":" + parsedArgs[key] + ",";
      }
    }
    queryStr = queryStr.slice(0, -1);
    queryStr += ")";
  }
  queryStr += "{" + fmtKeys(config.get("listFormat")) + "}";
  fmt = parseFormat(config.get("listFormat"));
  query(queryStr, config)
    .then(data => {
      data.filter = _.map(
        data.filter.sort((a, b) => b.urg - a.urg),
        genPrintKeys
      );
      printData = {};
      fmt.forEach(fmt => {
        printData[fmt.key] = [];
        data.filter.forEach(task => {
          printData[fmt.key].push(fmtData(fmt, task));
        });
        const longest = _.max(printData[fmt.key], str => str.length).length;
        if (longest === 0) delete printData[fmt.key];
        else
          printData[fmt.key] = _.map(printData[fmt.key], str => {
            if (fmt.align === "<") return str.padEnd(longest);
            else return str.padStart(longest);
          });
      });
      for (const i in data.filter) {
        var line = "";
        for (const key in printData) {
          line += "  " + printData[key][i];
        }
        if (i % 2 === 0)
          console.log(
            urgColor(data.filter[i].urg, data.filter[i].active)(line)
          );
        else
          console.log(
            chalk.bgBlack(
              urgColor(data.filter[i].urg, data.filter[i].active)(line)
            )
          );
      }
    })
    .catch(err => error);
};
