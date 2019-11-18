#!/usr/bin/env node

const argparse = require('./argparse.js');

const rxDue = /((?<=(d:|due:))\S+)/;
const rxPriority = /((?<=(p:|priority:))\S+)/;
const rxHidden = /((?<=(h:|hidden:))(true|t|f|false))/;
const rxUser = /((?<=(u:|user:))\S+)/;
const rxParent = /((?<=\+:)\S+)/;
const rxChild = /((?<=\_:)\S+)/;
const rxTag = /((?<=\@:)\S+)/;
args = argparse.parseArgs();
console.log(args);
