const _ = require("lodash");
const axios = require("axios");
const output = require("./output.js");
const select = require("./select.js");

module.exports.start = (config, args) => {
  axios
    .post(config.get("url") + "task/start/?token=" + config.get("token"), {
      ref: _.join(args.ref, " "),
      time: args.time || _.now(),
      ..._.omit(args, ["ref", "action", "nargs", "time"])
    })
    .then(res => {
      if ("data" in res.data)
        return select.select(res.data.data);
      else if ("error" in res.data) throw res.data.error;
      else
        return output.printTask(res.data.task);
    }).then(tsk => {
      return axios.post(config.get("url") + "task/start/?token=" + config.get("token"), {
        ref: tsk.uuid,
        time: args.time || _.now()
      });
    }).then(res => {
      if ("error" in res.data) throw res.data.error;
      else return output.printTask(res.data.task);
    })
    .catch(err => {
      return output.error(err);
    });
};
module.exports.startHelp = () => {
  return {
    usage: "start REF [TIME]",
    ref: "Reference to a task utilizing any of the referencing parameters.",
    time: "Start time of the task, using the standard date/time parameter options."
  };
};
module.exports.stop = (config, args) => {
  axios
    .post(config.get("url") + "task/stop/?token=" + config.get("token"), {
      ref: _.join(args.ref, " "),
      time: args.time || _.now(),
      ..._.omit(args, ["ref", "action", "nargs", "time"])
    })
    .then(res => {
      if ("data" in res.data)
        return select.select(res.data.data);
      else if ("error" in res.data) throw res.data.error;
      return output.printTask(res.data.task);
    }).then(tsk => {
      return axios.post(config.get("url") + "task/stop/?token=" + config.get("token"), {
        ref: tsk.uuid,
        time: args.time || _.now()
      });
    }).then(res => {
      if ("error" in res.data) throw res.data.error;
      else return output.printTask(res.data.task);
    })
    .catch(err => {
      return output.error(err);
    });
};
module.exports.stopHelp = () => {
  return {
    usage: "Stop REF [TIME]",
    ref: "Reference to a task utilizing any of the referencing parameters.",
    time: "Stop time of the task, using the standard date/time parameter options."
  };
};
module.exports.create = (config, args) => {
  axios
    .post(config.get("url") + "task/create/?token=" + config.get("token"), {
      title: _.join(args.ref, " "),
      ..._.omit(args, ["ref", "action", "nargs"])
    })
    .then(res => {
      if ("error" in res.data) throw res.data.error;
      return output.printTask(res.data.task);
    })
    .catch(err => {
      return output.error(err);
    });
};
module.exports.createHelp = () => {
  return {
    usage: "create REF [TIME]",
    ref: "Reference to a task utilizing any of the referencing parameters.",
    time: "Start time of the task, using the standard date/time parameter options."
  };
};
module.exports.delete = (config, args) => {
  console.log(args);
  axios
    .post(config.get("url") + "task/?token=" + config.get("token"), {
      ref: _.join(args.ref, " ")
    })
    .then(res => {
      if ("error" in res.data) throw res.data.error;
      if (res.data.length !== 1) throw "Multiple tasks matched, must specify a single task";
      return axios.post(config.get("url") + "task/delete/?token=" + config.get("token"), {
        uuid: res.data[0].uuid
      });
    })
    .then(res => {
      if ("error" in res.data) throw res.data.error;
      return output.msg('Deleted Task');
    })
    .catch(err => {
      return output.error(err);
    });
};
module.exports.deleteHelp = () => {
  return {
    usage: "delete REF",
    ref: "Reference to a task utilizing any of the referencing parameters."
  };
};

module.exports.detail = (config, args) => {
  axios
    .post(config.get("url") + "task/?token=" + config.get("token"), {
      ref: _.join(args.ref, " "),
      ..._.omit(args, ["ref", "action", "nargs"])
    })
    .then(res => {
      if ("error" in res.data) throw res.data.error;
      if (res.data.length !== 1) {
        return select.select(res.data);
      } else {
        return res.data[0];
      }
    }).then(task => {
      return output.printDetails(task);
    })
    .catch(err => {
      return output.error(err);
    });
}
module.exports.detailHelp = () => {
  return {
    usage: "create REF [TIME]",
    ref: "Reference to a task utilizing any of the referencing parameters.",
    time: "Start time of the task, using the standard date/time parameter options."
  };
};

module.exports.list = (config, args) => {
  axios
    .post(config.get("url") + "task/?token=" + config.get("token"), {
      ref: _.join(args.ref, " "),
      ..._.omit(args, ["ref", "action", "nargs"])
    })
    .then(res => {
      if ("error" in res.data) throw res.data.error;
      if (res.data.length === 1 && args.action === "root") {
        return output.printDetails(res.data[0]);
      } else {
        for (tsk in res.data) {
          output.printTask(res.data[tsk]);
        }
      }
    })
    .catch(err => {
      return output.error(err);
    });
};
module.exports.listHelp = () => {
  return {
    usage: "create REF [TIME]",
    ref: "Reference to a task utilizing any of the referencing parameters.",
    time: "Start time of the task, using the standard date/time parameter options."
  };
};

module.exports.login = (config, args) => {
  console.log(config.get("url") + "user/");
  axios
    .post(config.get("url") + "user/", {
      email: args.email
    })
    .then(res => {
      res = res.data;
      if ("error" in res && res.error == "user does not exist")
        return axios.post(config.get("url") + "user/create/", {
          email: args.email
        });
      else if ("error" in res) {
        throw res.error;
      } else {
        return new Promise((resolve, reject) =>
          resolve({
            data: {
              user: res
            }
          })
        );
      }
    })
    .then(res => {
      res = res.data;
      if ("error" in res) throw res.error;
      config.set("token", res.user.uuid);
      output.msg(`Logged in as "${args.email}"`);
    })
    .catch(err => {
      output.error(err);
    });
};
module.exports.loginHelp = () => {
  return {
    usage: "login EMAIL",
    email: "Email of user to login/create."
  };
};
module.exports.logout = (config, args) => {
  if (config.has("token")) config.delete("token");
  output.msg("Logged out of current user");
};
module.exports.logoutHelp = () => {
  return {
    usage: "logout"
  };
};
