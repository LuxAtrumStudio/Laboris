const axios = require("axios");

module.exports.get = (url, config) => {
  return axios.get(config.get("host") + "/api/" + url).then(res => res.data);
};

module.exports.post = (url, body, config) => {
  return axios
    .post(config.get("host") + "/api/" + url, body)
    .then(res => {
      var queue = config.get("queue");
      if (queue) {
        config.delete("queue");
        queue.forEach(req => {
          if (req[0] === "GET") this.get(req[0], config);
          else if (req[0] === "POST") this.post(req[0], req[1], config);
        });
      }
      return res.data;
    })
    .catch(err => {
      if (config.get("queue")) {
        config.set("queue", config.get("queue").concat([["POST", url, body]]));
      } else {
        config.set("queue", [["POST", url, body]]);
      }
      return err;
    });
};
