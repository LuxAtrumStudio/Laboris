const _ = require("lodash");
const moment = require("moment");
const chalk = require("chalk");
const { query, mutation, errors } = require("../graphql.js");
const { parseDate } = require("../common.js");
const { short } = require("../print.js");
const { printHelp, getTask } = require("../util.js");
const { duration } = require("../print.js");
const { parseFormat, fmtData } = require("../fmt.js");

module.exports = (args, config) => {
  if(args.help === true || args.h === true) {
    printHelp("reports detail TASK", "Displays detailed information for a specified task", {});
    return;
  } else if (args._.length === 0) {
    console.log(chalk.red.bold("  Must specify a task"));
  } else {
    getTask(_.join(args._, " "), config, id => {
      query(`get(id:\"${id}\"){id,title,parents{id,title},children{id,title},tags,priority,entryDate,dueDate,doneDate,modifiedDate,times,hidden,urg}`, config).then(data => {
        data = data.get;
        printData = {
          ...data,
          entryDate: moment(data.entryDate).format("YYYY-MM-DD HH:mm:ss"),
          dueDate: moment(data.entryDate).format("YYYY-MM-DD HH:mm:ss"),
          doneDate: moment(data.entryDate).format("YYYY-MM-DD HH:mm:ss"),
          modifiedDate: moment(data.entryDate).format("YYYY-MM-DD HH:mm:ss"),
          times: _.map(data.times, int => `${moment(int[0]).format("YYYY-MM-DD")}: ${moment(int[0]).format("HH:mm")}-${moment(int[1]).format("HH:mm")} [${duration(int[0], int[1])}]`),
          totalTime: duration(_.sum(_.map(data.times, int => int[1] - int[0]))),
          urg: fmtData({key: 'urg', type: 'f', precision: '3'}, data),
          priority: parseInt(data.priority).toString(),
          hidden: data.hidden ? 'True' : 'False',
          parents: _.map(data.parents, 'title'),
          children: _.map(data.children, 'title'),
        };
        var kLength = 0;
        var vLength = 0;
        for (const k in printData) {
          if (Array.isArray(printData[k])) {
            if(printData[k].length !== 0) vLength = Math.max(vLength, _.max(printData[k], o => o.length).length);
            else printData[k] = '';
          } else {
            vLength = Math.max(vLength, printData[k].length);
          }
          kLength = Math.max(kLength, k.length);
        }
        console.log(chalk.bold.underline(('  ' + printData.title).padEnd(kLength + vLength + 2)));
        var i = 0;
        for(const k in printData) {
          if(Array.isArray(printData[k])){
            if(i % 2 == 0)
              console.log(chalk.bold(k.padStart(kLength)) + '  ' + printData[k][0].padEnd(vLength));
            else
              console.log(chalk.bgBlack(chalk.bold(k.padStart(kLength)) + '  ' + printData[k][0].padEnd(vLength)));
            if(printData[k].length > 1) {
              i += 1;
              for(const j in printData[k]) {
                if(i % 2 == 0)
                  console.log(chalk.bold(''.padStart(kLength)) + '  ' + printData[k][j].padEnd(vLength));
                else
                  console.log(chalk.bgBlack(chalk.bold(''.padStart(kLength)) + '  ' + printData[k][j].padEnd(vLength)));
                i += 1;
              }
              i -= 1;
            }
          }else {
            if(i % 2 == 0)
              console.log(chalk.bold(k.padStart(kLength)) + '  ' + printData[k].padEnd(vLength));
            else
              console.log(chalk.bgBlack(chalk.bold(k.padStart(kLength)) + '  ' + printData[k].padEnd(vLength)));
          }
          i += 1;
        }
      }).catch(err => { console.log(err);});
    });
  }
}
