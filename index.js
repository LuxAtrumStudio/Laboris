#!/usr/bin/env node
const rxDue = /((?<=(d:|due:))\S+)/;
const rxPriority = /((?<=(p:|priority:))\S+)/;
const rxHidden = /((?<=(h:|hidden:))(true|t|f|false))/;
const rxUser = /((?<=(u:|user:))\S+)/;
const rxParent = /((?<=\+:)\S+)/;
const rxChild = /((?<=\_:)\S+)/;
const rxTag = /((?<=\@:)\S+)/;
const args = require("arg")(
  {
    "--help": Boolean,
    "--due": String,
    "--priority": Number,
    "--hidden": Boolean,
    "--user": [String],
    "--parent": [String],
    "--child": [String],
    "--tag": [String],
    "-p": "--priority",
    "-t": "--tag",
    "-d": "--due",
    "--dueDate": "--due"
  },
  { permissive: true }
);
console.log(args);
