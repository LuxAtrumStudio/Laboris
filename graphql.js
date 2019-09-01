const axios = require("axios");
const chalk = require("chalk");

const postData = (url, data) => {
  return axios.post(url, data).then(response => {
    return new Promise((resolve, reject) => {
      if ("errors" in response.data) reject(response.data.errors);
      else resolve(response.data.data);
    });
  });
};

module.exports.query = (query, config) => {
  return postData(config.get("host") + "/api/graphql", {
    query: "query {" + query + "}"
  });
};

module.exports.mutation = (mutation, config) => {
  return postData(config.get("host") + "/api/graphql", {
    query: "mutation {" + mutation + "}"
  });
};

module.exports.errors = err => {
  if (err.response && err.response.data && err.response.data.errors) {
    err.response.data.errors.forEach(msg => {
      console.log(
        chalk.yellow.bold(
          `  ${msg.message}(${msg.locations[0].line}:${msg.locations[0].column})`
        )
      );
    });
  } else if (err.code === "ECONNREFUSED") {
    console.log(chalk.yellow.bold("  Failed to connect to host"));
    console.log(
      chalk.yellow(
        "    Check that the host variable is set properyly in the configuration"
      )
    );
    console.log(chalk.yellow("    And that you have an internet connection"));
  } else {
    console.log(chalk.yellow.bold("  Unrecognized Error"));
    console.log(err);
  }
};
