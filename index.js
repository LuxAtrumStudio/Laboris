#!/usr/bin/env node
const argparse = require('./argparse.js');
const cli = require('./cli.js');

const args = argparse.parse();
console.log(args);
