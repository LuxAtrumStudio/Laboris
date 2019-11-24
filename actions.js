const _ = require("lodash");
const axios = require("axios");
const output = require("./output.js");

module.exports.start = (config, args) => {
  console.log(args);
  // axios.post(config.get("url") + "task/start/?token=" + config.get("token"), _.filter(args, (key) => key !== 'action' && key !== 'nargs' && key !== 'time');
};
module.exports.startHelp = () => {
  return {
    usage: "start REF [TIME]",
    ref: "Reference to a task utilizing any of the referencing parameters.",
    time:
      "Start time of the task, using the standard date/time parameter options."
  };
};
module.exports.create = (config, args) => {
  console.log(args);
  axios
    .post(config.get("url") + "task/create/?token=" + config.get("token"), {
      title: _.join(args.ref, " "),
      ..._.omit(args, ["ref", "action", "nargs"])
    })
    .then(res => {
      console.log(res.data);
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
    time:
      "Start time of the task, using the standard date/time parameter options."
  };
};

module.exports.list = (config, args) => {
  console.log(args);
  axios
    .post(config.get("url") + "task/?token=" + config.get("token"), {
      ..._.omit(args, ["ref", "action", "nargs"])
    })
    .then(res => {
      console.log(res.data);
      if ("error" in res.data) throw res.data.error;
      for (tsk in res.data) {
        output.printTask(res.data[tsk]);
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
    time:
      "Start time of the task, using the standard date/time parameter options."
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
