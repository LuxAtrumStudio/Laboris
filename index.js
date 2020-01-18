#!/usr/bin/env node

const _ = require("lodash");
const uuidv5 = require("uuid/v5");
const inquirer = require("inquirer");
const axios = require("axios");

const argparse = require("./argparse.js");
const datetime = require("./datetime.js");
const data = require("./data.js");
const config = require("./config.js");
const cliUtil = require("./cliUtil.js");
const moment = require("moment");

const createTask = args => {
  return data
    .load()
    .then(_data => {
      const taskUUID = uuidv5(args.ref + _.now().toString(), uuidv5.URL);
      data.tasks[taskUUID] = _.defaults(_.omit(args, "ref"), {
        uuid: taskUUID,
        title: args.ref,
        entryDate: _.now(),
        modifiedDate: _.now(),
        doneDate: null,
        dueDate: null,
        times: [],
        open: true,
        urg: 0.0
      });
      return Promise.all([
        Promise.resolve(taskUUID),
        Promise.resolve(_.uniq(_.concat(args.parents, args.children))),
        ..._.map(_.uniq(_.concat(args.parents, args.children)), tsk =>
          data.getUUID({
            ref: tsk
          })
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
      cliUtil.printCreate(data.tasks[taskUUID]);
      return data.create(taskUUID);
    })
    .then(data.save);
};
const deleteTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.pull)
    .then(taskUUID => {
      return inquirer.prompt([{
        type: "confirm",
        name: taskUUID,
        message: `Are you sure you want to delete ${data.tasks[
            taskUUID
          ].uuid.slice(0, 8)}  [${data.tasks[taskUUID].title}]?`,
        default: false
      }]);
    })
    .then(answ => {
      let deletedId = undefined;
      let tmpTask = undefined;
      const updated = [];
      for (const id in answ) {
        if (answ[id] === true) {
          deletedId = data.tasks[id].uuid;
          for (const parent of data.tasks[id].parents) {
            updated.push(parent);
            _.pull(data.tasks[parent].children, deletedId);
          }
          for (const child of data.tasks[id].children) {
            updated.push(child);
            _.pull(data.tasks[child].parents, deletedId);
          }
          tmpTask = data.tasks[id];
          delete data.tasks[id];
        }
      }
      if (tmpTask !== undefined) {
        cliUtil.printDelete(tmpTask);
        return Promise.all([
          data.delete(deletedId),
          ..._.map(updated, id => data.push(id))
        ]);
      } else {
        return undefined;
      }
    })
    .then(data.save);
};

const startTask = args => {
  return data
    .load()
    .then(_data => {
      return data.filterTasks(_.omit(args, "active"));
    })
    .then(tasks => {
      return data.pull(_.map(tasks, "uuid"));
    })
    .then(tasks => {
      return data.getUUID(
        args,
        _.map(tasks, id => data.tasks[id])
      );
    })
    .then(taskUUID => {
      data.tasks[taskUUID].modifiedDate = _.now();
      data.tasks[taskUUID].times.push(args.time);
      cliUtil.printStart(data.tasks[taskUUID]);
      return data.push(taskUUID);
    })
    .then(data.save);
};
const stopTask = args => {
  return data
    .load()
    .then(_data => {
      return data.filterTasks(_.omit(args, "active"));
    })
    .then(tasks => {
      return data.pull(_.map(tasks, "uuid"));
    })
    .then(tasks => {
      return data.getUUID(
        args,
        _.map(tasks, id => data.tasks[id])
      );
    })
    .then(taskUUID => {
      data.tasks[taskUUID].modifiedDate = _.now();
      data.tasks[taskUUID].times.push(args.time);
      cliUtil.printStop(data.tasks[taskUUID]);
      return data.push(taskUUID);
    })
    .then(data.save);
};
const closeTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.pull)
    .then(taskUUID => {
      data.tasks[taskUUID].modifiedDate = _.now();
      data.tasks[taskUUID].open = false;
      cliUtil.printClose(data.tasks[taskUUID]);
      return data.push(taskUUID);
    })
    .then(data.save);
};
const openTask = args => {
  return data
    .load()
    .then(_data => {
      return data.getUUID(args);
    })
    .then(data.pul)
    .then(taskUUID => {
      data.tasks[taskUUID].modifiedDate = _.now();
      data.tasks[taskUUID].open = true;
      cliUtil.printOpen(data.tasks[taskUUID]);
      return data.push(taskUUID);
    })
    .then(data.save);
};

const reportShowList = tasks => {
  return new Promise((resolve, reject) => {
    table = [];
    tasks = _.reverse(_.sortBy(tasks, "urg"));
    for (const task of tasks) {
      table.push(cliUtil.formatList(task));
    }
    cliUtil.printTable(table, [], true);
    resolve(undefined);
  });
};
const reportShowDetail = task => {
  return new Promise((resolve, reject) => {
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
    if (task.dueDate !== null) {
      table.push([
        titleFunc("Due Date"),
        moment(task.dueDate).format("YYYY-MM-DD HH:mm:ss")
      ]);
    }
    if (task.doneDate !== null) {
      table.push([
        titleFunc("Done Date"),
        moment(task.doneDate).format("YYYY-MM-DD HH:mm:ss")
      ]);
    }
    if (task.modifiedDate !== undefined) {
      table.push([
        titleFunc("Modified Date"),
        moment(task.modifiedDate).format("YYYY-MM-DD HH:mm:ss")
      ]);
    }
    if (task.tags.length !== 0) {
      for (let i in task.tags) {
        i = _.toInteger(i);
        if (i === 0) table.push([titleFunc("Tags"), task.tags[i]]);
        else table.push(["", task.tags[i]]);
      }
    }
    if (task.parents.length !== 0) {
      for (let i in task.parents) {
        i = _.toInteger(i);
        if (i === 0) {
          table.push([
            titleFunc("Parents"),
            cliUtil.formatShort(data.tasks[task.parents[i]])
          ]);
        } else
          table.push(["", cliUtil.formatShort(data.tasks[task.parents[i]])]);
      }
    }
    if (task.children.length !== 0) {
      for (let i in task.children) {
        i = _.toInteger(i);
        if (i === 0) {
          table.push([
            titleFunc("Children"),
            cliUtil.formatShort(data.tasks[task.children[i]])
          ]);
        } else {
          table.push(["", cliUtil.formatShort(data.tasks[task.children[i]])]);
        }
      }
    }
    if (task.times.length !== 0) {
      for (let i of _.range(0, task.times.length, 2)) {
        i = _.toInteger(i);
        if (i === 0) {
          table.push([
            titleFunc("Times"),
            datetime.formatInterval(
              task.times[i],
              task.times.length > i + 1 ? task.times[i + 1] : _.now()
            )
          ]);
        } else {
          table.push([
            "",
            datetime.formatInterval(
              task.times[i],
              task.times.length > i + 1 ? task.times[i + 1] : _.now()
            )
          ]);
        }
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
      if (tasks.length === 1) {
        return reportShowDetail(tasks[Object.keys(tasks)[0]]);
      } else return reportShowList(tasks);
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

const userCreate = args => {
  return axios
    .post(config.get("remoteUrl") + "user/create/", args)
    .then(response => {
      if (response.data.error !== undefined) {
        return cliUtil.printError(response.data.error);
      }
      cliUtil.printSuccess(response.data.success);
      config.set("uuid", response.data.uuid);
    })
    .catch(err => {
      console.error(err);
    });
};

const userSignin = args => {
  return axios
    .post(config.get("remoteUrl") + "user/signin/", args)
    .then(response => {
      if (response.data.error !== undefined) {
        return cliUtil.printError(response.data.error);
      }
      cliUtil.printSuccess(response.data.success);
      config.set("uuid", response.data.uuid);
    });
};
const userSignout = args => {
  return new Promise((resolve, reject) => {
    if (config.has("uuid")) config.delete("uuid");
    cliUtil.printSuccess("Signed out of user");
    resolve();
  });
};

const user = (action, args) => {
  return new Promise((resolve, reject) => {
    if (action === "create") return userCreate(args);
    if (action === "signin") return userSignin(args);
    if (action === "signout") return userSignout(args);
  });
};

const configCmd = args => {
  return new Promise((resolve, reject) => {
    for (const key of args.keys) {
      cliUtil.printNote(
        `Config value "${key}" = ${JSON.stringify(config.get(key))}`
      );
    }
    for (const key in args.set) {
      config.set(key, args.set[key]);
      cliUtil.printSuccess(`Set config value "${key}" = ${args.set[key]}`);
    }
  });
};

const sync = args => {
  return data
    .load()
    .then(_data => {
      return data.sync(args);
    })
    .then(_data => {
      cliUtil.printSuccess(
        `Synced tasks with remote server at ${datetime.formatDate(
          _.now(),
          "YYYY-MM-DD HH:mm:ss"
        )}`
      );
      return data.save();
    });
};

argparse()
  .then(cmd => {
    if (cmd === undefined) return undefined;
    else if (cmd.command === "create") return createTask(cmd.args);
    else if (cmd.command === "delete") return deleteTask(cmd.args);
    else if (cmd.command === "start") return startTask(cmd.args);
    else if (cmd.command === "stop") return stopTask(cmd.args);
    else if (cmd.command === "open") return openTask(cmd.args);
    else if (cmd.command === "close") return closeTask(cmd.args);
    else if (cmd.command === "report") return report(cmd.report, cmd.args);
    else if (cmd.command === "user") return user(cmd.action, cmd.args);
    else if (cmd.command === "config") return configCmd(cmd.args);
    else if (cmd.command === "sync") return sync(cmd.args);
  })
  .catch(err => {
    if (_.isObject(err)) {
      console.log(err);
      if ("error" in err) cliUtil.printError(err.error);
      else if ("warning" in err) cliUtil.printNote(err.warning);
      else cliUtil.printError(`Unrecognized Error: ${err}`);
    } else {
      cliUtil.printError(err);
    }
  });
