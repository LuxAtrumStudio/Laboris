#!/usr/bin/env node
const _ = require("lodash");
const uuidv5 = require("uuid/v5");
const inquirer = require("inquirer");

const argparse = require("./argparse.js");
const data = require("./data.js");
const config = require("./config.js");
const cliUtil = require("./cliUtil.js");
const moment = require("moment");

const createTask = args => {
  return data
    .load()
    .then(_data => {
      const taskUUID = uuidv5(args.ref + _.now().toString(), uuidv5.URL);
      data.tasks[taskUUID] = _.defaults(args, {
        uuid: taskUUID,
        title: args.ref,
        entryDate: _.now(),
        modifiedDate: _.now(),
        syncTime: _.now(),
        doneDate: null,
        dueDate: null,
        times: [],
        open: true
      });
      return Promise.all([
        Promise.resolve(taskUUID),
        Promise.resolve(_.uniq(_.concat(args.parents, args.children))),
        ..._.map(_.uniq(_.concat(args.parents, args.children)), tsk =>
          data.getUUID({ ref: tsk })
        )
      ]);
    })
    .then(uuids => {
      taskUUID = uuids[0];
      keys = uuids[1];
      uuids = _.slice(uuids, 2);
      for (const i in data.tasks[taskUUID].parents) {
        for (const j in keys) {
          if (data.tasks[taskUUID].parents[i] === keys[j]) {
            data.tasks[taskUUID].parents[i] = uuids[j];
            data.tasks[uuids[j]].children.push(taskUUID);
          }
        }
      }
      for (const i in data.tasks[taskUUID].children) {
        for (const j in keys) {
          if (data.tasks[taskUUID].children[i] === keys[j]) {
            data.tasks[taskUUID].children[i] = uuids[j];
            data.tasks[uuid[j]].parents.push(taskUUID);
          }
        }
      }
      return data.sync(taskUUID);
    })
    .then(data.save);
};
const deleteTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.fetch)
    .then(taskUUID => {
      return inquirer.prompt([
        {
          type: "confirm",
          name: taskUUID,
          message: `Are you sure you want to delete ${data.tasks[
            taskUUID
          ].uuid.slice(0, 8)}  [${data.tasks[taskUUID].title}]?`,
          default: false
        }
      ]);
    })
    .then(answ => {
      let deletedId = undefined;
      for (const id in answ) {
        if (answ[id] === true) {
          deletedId = data.tasks[id].uuid;
          for (const parent of data.tasks[id].parents) {
            _.pull(data.tasks[parent].children, deletedId);
          }
          for (const child of data.tasks[id].children) {
            _.pull(data.tasks[child].parents, deletedId);
          }
          delete data.tasks[id];
        }
      }
      return data.syncDelete(deletedId);
    })
    .then(data.save);
};

const startTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.fetch)
    .then(taskUUID => {
      data.tasks[taskUUID].times.push(args.time);
      return data.sync(taskUUID);
    })
    .then(data.save);
};
const stopTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.fetch)
    .then(taskUUID => {
      data.tasks[taskUUID].times.push(args.time);
      return data.sync(taskUUID);
    })
    .then(data.save);
};
const closeTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.fetch)
    .then(taskUUID => {
      data.tasks[taskUUID].open = false;
      return data.sync(taskUUID);
    })
    .then(data.save);
};
const openTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.fetch)
    .then(taskUUID => {
      data.tasks[taskUUID].open = true;
      return data.sync(taskUUID);
    })
    .then(data.save);
};

const reportShowList = tasks => {
  return new Promise((resolve, reject) => {
    table = [];
    for (const task of tasks) {
      table.push(cliUtil.formatList(task));
    }
    cliUtil.printTable(table, [], true);
    resolve(undefined);
  });
};
const reportShowDetail = task => {
  return new Promise((resolve, reject) => {
    console.log("DETAIL", task);
    table = [];
    const titleFunc = cliUtil.getColorFunc(config.getColor("title"));
    table.push([titleFunc("Title"), task.title]);
    table.push([titleFunc("UUID"), task.uuid]);
    table.push([titleFunc("Urg"), task.urg.toFixed(3)]);
    table.push([titleFunc("Priority"), task.priority.toString()]);
    table.push([
      titleFunc("Entry Date"),
      moment(task.entryDate).format("YYYY-MM-DD HH:mm:ss")
    ]);
    if (task.dueDate !== null)
      table.push([
        titleFunc("Due Date"),
        moment(task.dueDate).format("YYYY-MM-DD HH:mm:ss")
      ]);
    if (task.doneDate !== null)
      table.push([
        titleFunc("Done Date"),
        moment(task.doneDate).format("YYYY-MM-DD HH:mm:ss")
      ]);
    if (task.modifiedDate !== undefined)
      table.push([
        titleFunc("Modified Date"),
        moment(task.modifiedDate).format("YYYY-MM-DD HH:mm:ss")
      ]);
    if (task.times.length !== 0) {
      const fmtInterval = i => {
        let a = task.times[i];
        let b = task.times.length > i + 1 ? task.times[i + 1] : _.now();
        let aMoment = moment(a);
        let bMoment = moment(b);
        if (bMoment.diff(aMoment, "days") !== 0) {
          return (
            aMoment.format("YYYY-MM-DD HH:mm") +
            " - " +
            bMoment.format("YYYY-MM-DD HH:mm")
          );
        } else {
          return (
            aMoment.format("YYYY-MM-DD HH:mm") + " - " + bMoment.format("HH:mm")
          );
        }
      };
      for (const i in _.range(0, task.times.length, 2)) {
        if (i == 0) table.push([titleFunc("Times"), fmtInterval(i)]);
        else table.push(["", fmtInterval(i)]);
      }
    }

    cliUtil.printTable(table, [], true);
    resolve(undefined);
  });
};

const reportAutolist = args => {
  return data
    .load()
    .then(_data => {
      return data.filterTasks(args);
    })
    .then(tasks => {
      if (tasks.length === 1)
        return reportShowDetail(tasks[Object.keys(tasks)[0]]);
      else return reportShowList(tasks);
    });
};

const reportList = args => {
  return data
    .load()
    .then(_data => {
      return data.filterTasks(args);
    })
    .then(tasks => {
      return reportShowList(tasks);
    });
};
const reportDetail = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(taskUUID => {
      return reportShowDetail(data.tasks[taskUUID]);
    });
};

const report = (report, args) => {
  return new Promise((resolve, reject) => {
    if (report === "autolist") return reportAutolist(args);
    if (report === "list") return reportList(args);
    if (report === "detail") return reportDetail(args);
  });
};

argparse()
  .then(cmd => {
    console.log(cmd);
    if (cmd === undefined) return undefined;
    else if (cmd.command === "create") return createTask(cmd.args);
    else if (cmd.command === "delete") return deleteTask(cmd.args);
    else if (cmd.command === "start") return startTask(cmd.args);
    else if (cmd.command === "stop") return stopTask(cmd.args);
    else if (cmd.command === "open") return openTask(cmd.args);
    else if (cmd.command === "close") return closeTask(cmd.args);
    else if (cmd.command === "report") return report(cmd.report, cmd.args);
  })
  .catch(err => {
    console.error(err);
  });
