#!/usr/bin/env node

const argparse = require('./argparse.js');
argparse()
    .then(cmd => {
      console.log(cmd);
    })
    .catch(err => {
      console.error(err);
    });