#!/usr/bin/env node

const Configstore = require("configstore");

const argparse = require("./argparse.js");
const actions = require("./actions.js");
const output = require("./output.js");

const config = new Configstore("laboris", {
  url: "https://laboris.luxater.com/"
});

const rootHelp = () => {
  return {
    usage: "laboris"
  };
};

args = argparse.parseArgs();
if (args.action !== "login" && args.action !== "help" && !config.has("token"))
  return output.error("Must login before usage");

if (args.action === "start") return actions.start(config, args);
else if (args.action === "stop") return actions.stop(config, args);
else if (args.action === "login") return actions.login(config, args);
else if (args.action === "logout") return actions.logout(config, args);
else if (args.action === "create") return actions.create(config, args);
else if (args.action === "delete") return actions.delete(config, args);
else if (args.action === "list") return actions.list(config, args);
else if (args.action === "detail") return actions.detail(config, args);
else if (args.action === "root") return actions.list(config, args);
else if (args.action == "help") {
  if (args.module == "start") return output.fmtHelp(actions.startHelp());
  else if (args.module == "stop") return output.fmtHelp(actions.stopHelp());
  else if (args.module == "login") return output.fmtHelp(actions.loginHelp());
  else if (args.module == "logout") return output.fmtHelp(actions.logoutHelp());
  else if (args.module == "create") return output.fmtHelp(actions.createHelp());
  else if (args.module == "delete") return output.fmtHelp(actions.deleteHelp());
  else if (args.module == "list") return output.fmtHelp(actions.listHelp());
  else if (args.module == "detail") return output.fmtHelp(actions.detailHelp());
  else if (args.module == "root") return output.fmtHelp(rootHelp());
}
