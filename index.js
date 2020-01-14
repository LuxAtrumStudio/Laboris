#!/usr/bin/env node
const _ = require('lodash');
const argparse = require('./argparse.js');
const cli = require('./cli.js');
const commands = require('./commands.js');

const args = argparse.parse();

console.log(args);

if (args === undefined)
  return;
else if (args.command === 'config') {
  if (args.set === undefined) {
    cli.printNote(`Config Value: ${args.value}: ${cli.config.get(args.value)}`);
  } else if (args.set !== undefined) {
    cli.config.set(args.value, args.set);
    cli.printNote(
        `Set Config Value: ${args.value}: ${cli.config.get(args.value)}`);
  }
} else if (args.command === 'user') {
  if (args.action === 'signin') {
    commands.user.signin(cli.config, args).catch(err => cli.printError(err));
  } else if (args.action === 'signout') {
    commands.user.signout(cli.config, args).catch(err => cli.printError(err));
  } else if (args.action === 'create') {
    commands.user.create(cli.config, args).catch(err => cli.printError(err));
  } else if (args.action === 'delete') {
    cli.printError('User Delete is not yet implemented');
  }
} else if (args.command === 'create') {
  commands.create(cli.config, cli.local, _.omit(args, 'command', 'action'))
      .catch(err => console.log(err));
  cli.printError('Create is not yet implemented');
} else if (args.command === 'modify') {
  cli.printError('Modify is not yet implemented');
} else if (args.command === 'start') {
  cli.printError('Start is not yet implemented');
} else if (args.command === 'stop') {
  cli.printError('Stop is not yet implemented');
} else if (args.command === 'close') {
  cli.printError('Close is not yet implemented');
} else if (args.command === 'open') {
  cli.printError('Open is not yet implemented');
} else if (args.command === 'report') {
  cli.printError('Reports are not yet implemented');
}