const _ = require("lodash");
const config = require("./config.js");
const fs = require("fs");
const path = require("path");
const Fuse = require("fuse.js");
const moment = require("moment");
const inquirer = require("inquirer");
const cliUtil = require("./cliUtil.js");
const axios = require("axios");

inquirer.registerPrompt(
  "autocomplete",
  require("inquirer-autocomplete-prompt")
);

const calcUrgDueDate = task => {
  if (!task.dueDate) return 0.0;
  const daysDue = (_.now() - task.dueDate) / 86400000;
  const totalActive = (task.dueDate - task.entryDate) / 86400000;
  const a = -4.39449 / totalActive;
  const b = -2.19722 / a;
  return 1.0 / (1 + Math.exp(a * (daysDue + b)));
};

const calculateUrg = task => {
  if (task.priority === 0 || task.open === false) return 0.0;
  let urg = 0.0;
  urg += Math.abs((0.01429 * (_.now() - task.entryDate)) / 86400000);
  urg += Math.abs(9.0 * calcUrgDueDate(task));
  urg += Math.abs(1.0 * task.parents.length);
  urg += Math.abs(0.2 * task.children.length);
  urg += Math.abs(0.2 * task.tags.length);
  urg += Math.abs(-2.0 * task.priority + 10);
  urg += Math.abs(4.0 * (task.times.length % 2 === 1));
  return urg;
};

module.exports.tasks = {};
module.exports.load = () => {
  return new Promise((resolve, _reject) => {
    fs.exists(config.get("dataFile"), exists => {
      resolve(exists);
    });
  })
    .then(exists => {
      return new Promise((resolve, reject) => {
        if (!exists) resolve({});
        else {
          fs.readFile(config.get("dataFile"), "utf8", (err, data) => {
            if (err) return reject(err);
            return resolve(JSON.parse(data));
          });
        }
      });
    })
    .then(data => {
      return new Promise(resolve => {
        for (const id in data) {
          this.tasks[id] = {
            ...data[id],
            urg: calculateUrg(data[id])
          };
        }
        resolve(this.tasks);
      });
    });
};
module.exports.save = () => {
  return new Promise((resolve, _reject) => {
    fs.exists(path.dirname(config.get("dataFile")), exists => {
      resolve(exists);
    });
  })
    .then(exists => {
      return new Promise((resolve, reject) => {
        if (!exists) {
          fs.mkdir(path.dirname(config.get("dataFile")), err => {
            if (err) return reject(err);
            else return resolve();
          });
        } else return resolve();
      });
    })
    .then(() => {
      return new Promise((resolve, reject) => {
        fs.writeFile(
          config.get("dataFile"),
          JSON.stringify(this.tasks),
          err => {
            if (err) return reject(err);
            else return resolve();
          }
        );
      });
    });
};
module.exports.pull = uuid => {
  return new Promise((resolve, reject) => {
    if (config.has("uuid")) {
      return axios
        .post(
          config.get("remoteUrl") +
            "tasks/pull/" +
            "?user=" +
            config.get("uuid"),
          { tasks: _.castArray(uuid) }
        )
        .then(response => {
          if ("error" in response.data) reject(response.data.error);
          for (const resUuid in response.data) {
            this.tasks[resUuid] = response.data[resUuid];
          }
          resolve(uuid);
        })
        .catch(err => {
          reject(err);
        });
    } else {
      return Promise((resolve, reject) => {
        resolve(uuid);
      });
    }
  });
};
module.exports.push = uuid => {
  return new Promise((resolve, reject) => {
    if (config.has("uuid")) {
      return axios
        .post(
          config.get("remoteUrl") +
            "tasks/push/" +
            "?user=" +
            config.get("uuid") +
            "&task=" +
            uuid,
          this.tasks[uuid]
        )
        .then(response => {
          if ("error" in response.data) reject(response.data.error);
          this.tasks[uuid] = response.data;
          resolve(uuid);
        });
    } else {
      return new Promise((resolve, reject) => {
        resolve(uuid);
      });
    }
  });
};
module.exports.create = uuid => {
  return new Promise((resolve, reject) => {
    if (config.has("uuid")) {
      return axios
        .post(
          config.get("remoteUrl") +
            "tasks/create/?user=" +
            config.get("uuid") +
            "&task=" +
            uuid,
          this.tasks[uuid]
        )
        .then(response => {
          if ("error" in response.data) reject(response.data.error);
          resolve(uuid);
        });
    } else {
      return new Promise((resolve, reject) => {
        resolve(uuid);
      });
    }
  });
};
module.exports.delete = uuid => {
  return new Promise((resolve, reject) => {
    if (config.has("uuid")) {
      return axios
        .post(
          config.get("remoteUrl") +
            "tasks/delete/" +
            "?user=" +
            config.get("uuid") +
            "&task=" +
            uuid
        )
        .then(response => {
          if ("error" in response.data) reject(response.data.error);
          resolve(uuid);
        });
    } else {
      return new Promise(resolve => {
        resolve(uuid);
      });
    }
  });
};
module.exports.sync = args => {
  return new Promise((resolve, reject) => {
    if (config.has("uuid")) {
      const url =
        config.get("remoteUrl") + "user/tasks/?user=" + config.get("uuid");
      return axios
        .get(url)
        .then(response => {
          if ("error" in response.data) reject(response.data.error);
          return this.pull(
            _.uniq(
              _.concat(
                _.difference(response.data.tasks, Object.keys(this.tasks)),
                args.open ? _.filter(this.tasks, tsk => tsk.open) : [],
                args.closed ? _.filter(this.tasks, tsk => !tsk.open) : []
              )
            )
          ).then(result => {
            resolve(this.tasks);
          });
        })
        .catch(err => {
          reject(err);
        });
    } else {
      return new Promsie(ressolve => {
        resolve(this.tasks);
      });
    }
  });
};
module.exports.filterTasks = (filter, tasks = this.tasks) => {
  return new Promise((resolve, reject) => {
    const filters = [];
    if (filter.parents !== undefined) {
      filters.push(o => _.difference(filter.parents, o.parents).length === 0);
    }
    if (filter.children !== undefined) {
      filters.push(o => _.difference(filter.children, o.children).length === 0);
    }
    if (filter.tags !== undefined) {
      filters.push(o => _.difference(filter.tags, o.tags).length === 0);
    }
    if (filter.open !== undefined) filters.push(o => o.open === filter.open);
    if (filter.hidden !== undefined) {
      filters.push(o => o.hidden === filter.hidden);
    }
    if (filter.active !== undefined) {
      filters.push(o => o.times.length % 2 === (filter.active ? 1 : 0));
    }
    if (filter.priority !== undefined) {
      filters.push(o => o.priority === filter.priority);
    }
    if (filter.priorityG !== undefined) {
      filters.push(o => o.priority > filter.priorityG);
    }
    if (filter.priorityL !== undefined) {
      filters.push(o => o.priority < filter.priorityL);
    }
    if (filter.parentCount !== undefined) {
      filters.push(o => o.parents.length === filter.parentCount);
    }
    if (filter.parentCountG !== undefined) {
      filters.push(o => o.parents.length > filter.parentCountG);
    }
    if (filter.parentCountL !== undefined) {
      filters.push(o => o.parents.length < filter.parentCountL);
    }
    if (filter.childCount !== undefined) {
      filters.push(o => o.children.length === filter.childCount);
    }
    if (filter.childCountG !== undefined) {
      filters.push(o => o.children.length > filter.childCountG);
    }
    if (filter.childCountL !== undefined) {
      filters.push(o => o.children.length < filter.childCountL);
    }
    if (filter.tagCount !== undefined) {
      filters.push(o => o.tags.length === filter.tagCount);
    }
    if (filter.tagCountG !== undefined) {
      filters.push(o => o.tags.length > filter.tagCountG);
    }
    if (filter.tagCountL !== undefined) {
      filters.push(o => o.tags.length < filter.tagCountL);
    }
    if (filter.due !== undefined) {
      filters.push(
        o =>
          o.dueDate !== null &&
          moment(o.dueDate).diff(moment(filter.due), "days") === 0
      );
    }
    if (filter.dueBefore !== undefined) {
      filters.push(o => o.dueDate !== null && o.dueDate < filter.dueBefore);
    }
    if (filter.dueAfter !== undefined) {
      filters.push(o => o.dueDate !== null && o.dueDate > filter.dueAfter);
    }
    if (filter.entry !== undefined) {
      filters.push(
        o =>
          o.entryDate !== null &&
          moment(o.entryDate).diff(moment(filter.entry), "days") === 0
      );
    }
    if (filter.entryBefore !== undefined) {
      filters.push(
        o => o.entryDate !== null && o.entryDate < filter.entryBefore
      );
    }
    if (filter.entryAfter !== undefined) {
      filters.push(
        o => o.entryDate !== null && o.entryDate > filter.entryAfter
      );
    }
    if (filter.done !== undefined) {
      filters.push(
        o =>
          o.doneDate !== null &&
          moment(o.doneDate).diff(moment(filter.done), "days") === 0
      );
    }
    if (filter.doneBefore !== undefined) {
      filters.push(o => o.doneDate !== null && o.doneDate < filter.doneBefore);
    }
    if (filter.doneAfter !== undefined) {
      filters.push(o => o.doneDate !== null && o.doneDate > filter.doneAfter);
    }
    if (filter.modified !== undefined) {
      filters.push(
        o =>
          o.modifiedDate !== null &&
          moment(o.modifiedDate).diff(moment(filter.modified), "days") === 0
      );
    }
    if (filter.modifiedBefore !== undefined) {
      filters.push(
        o => o.modifiedDate !== null && o.modifiedDate < filter.modifiedBefore
      );
    }
    if (filter.modifiedAfter !== undefined) {
      filters.push(
        o => o.modifiedDate !== null && o.modifiedDate > filter.modifiedAfter
      );
    }
    resolve(_.filter(tasks, o => _.every(_.map(filters, f => f(o)))));
  }).then(tasks => {
    return new Promise(resolve => {
      const fuse = new Fuse(tasks, {
        shouldSort: true,
        threshold: 0.5,
        keys: ["uuid", "title"]
      });
      if (filter.ref === "") return resolve(tasks);
      return resolve(fuse.search(filter.ref));
    });
  });
};
module.exports.getTitle = uuid => {
  return this.tasks[uuid].title;
};
module.exports.getUUID = (filter, tasks = this.tasks) => {
  return this.filterTasks(filter, tasks).then(tasks => {
    return new Promise((resolve, reject) => {
      if (tasks.length === 0) {
        return reject({
          warning: "No tasks satisfied all filters"
        });
      }
      if (tasks.length === 1) return resolve(tasks[0].uuid);
      const strings = {};
      for (const task of tasks) {
        strings[task.uuid] = cliUtil.formatShort(task);
      }
      const fuse = new Fuse(tasks, {
        shouldSort: true,
        threshold: 0.8,
        keys: ["uuid", "title"]
      });
      return resolve(
        inquirer
          .prompt([
            {
              type: "autocomplete",
              name: "uuid",
              message: "Specify Task",
              source: (_tmp, input) => {
                return new Promise((resolve, _reject) => {
                  if (input === undefined) {
                    return resolve(_.map(tasks, o => strings[o.uuid]));
                  }
                  const opt = fuse.search(input);
                  return resolve(
                    _.map(fuse.search(input), o => strings[o.uuid])
                  );
                });
              }
            }
          ])
          .then(answ => {
            for (const uuid in strings) {
              if (strings[uuid] === answ.uuid) return uuid;
            }
            return undefined;
          })
      );
    });
  });
};
