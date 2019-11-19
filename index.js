#!/usr/bin/env node

const argparse = require('./argparse.js');

args = argparse.parseArgs();
console.log(args);
