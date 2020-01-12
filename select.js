const _ = require("lodash");
const axios = require("axios");
const output = require("./output.js");
const inquirer = require('inquirer');
const Fuse = require("fuse.js");

inquirer.registerPrompt('autocomplete', require('inquirer-autocomplete-prompt'));

const getStr = (task, strings) => {
  for(const str in strings) {
    if (task.uuid == strings[str].uuid)
      return str
  }
}

module.exports.select = (tasks) => {
  let strings = {}
  for(const id in tasks) {
    strings[output.formatTask(tasks[id])] = tasks[id];
  }
  var fuse = new Fuse(tasks, {
    shouldSort: true,
    threshold: 1.0,
    location: 0,
    distance: 26,
    maxPatternLength: 32,
    keys: ['uuid', 'title', 'tags']
  });
  return inquirer.prompt([{
    type: "autocomplete",
    name: "task_ref",
    message: "Specify matched task",
    source: (tmp, input) => {
      return new Promise((resolve, reject) => {
        let opt = fuse.search(input);
        if(opt.length === 0)
          opt = tasks
        resolve(_.map(opt, o => getStr(o, strings)));
      });
    }
  }]).then(answ => {
    return strings[answ["task_ref"]];
  });
}
