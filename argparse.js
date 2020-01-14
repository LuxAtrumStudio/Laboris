const _ = require('lodash');

const wrapText = (str, width = 80, indent = 2, initIndent = 0) => {
  str = str.split(' ');
  res = '';
  line = ' '.repeat(initIndent);
  for (const word of str) {
    if ((line + word).length > width) {
      res += line + '\n';
      line = ' '.repeat(indent);
    }
    line += word + ' ';
  }
  res += line;
  return res;
};
const formatTable = (table, alignment = []) => {
  let colWidth = [];
  for (const r in table) {
    for (const c in table[r]) {
      if (c >= colWidth.length)
        colWidth.push(table[r][c].length);
      else
        colWidth[c] = Math.max(colWidth[c], table[r][c].length);
    }
  }
  if (alignment.length === 0) alignment = ['<'] * colWidth.length;
  let output = '';
  for (const r in table) {
    let line = '';
    for (const c in table[r]) {
      if (c !== 0) line += '  ';
      if (alignment[c] == '<')
        line += table[r][c].padEnd(colWidth[c], ' ');
      else if (alignment[c] == '>')
        line += table[r][c].padStart(colWidth[c], ' ');
    }
    output += line + '\n';
  }
  return output;
};

class ArgumentParser {
  constructor(name, description = null, allowUnknown = false, parent = null) {
    this.name = name;
    this.description = description;
    this.arguments = {};
    this.subparsers = {};
    this.allowUnknown = allowUnknown;
    this.defaultSubParser = null;
    this.parent = parent;
  }
  setDefaultSubparser(name) {
    this.defaultSubParser = name;
  }
  addArgument(name, options = {}) {
    const destName = options.dest !== undefined ?
        options.dest :
        _.trim(_.last(_.split(name, ',')), '_-+@ ');
    this.arguments[destName] = _.defaults(options, {
      names: _.map(_.split(name, ','), str => _.trim(str)),
      positional: (['-', '+', '@'].includes(name[0])) ? false : true,
      action: 'store',
      nargs: 1,
      default: null,
      type: String,
      choices: null,
      required: false,
      help: '',
      metavar: _.toUpper(destName),
      dest: destName
    });
    return this;
  }
  addSubparser(name, options = {}) {
    this.subparsers[name] = _.defaults(options, {
      name: name,
      alias: [],
      parser: new ArgumentParser(name, options.help, this.allowUnknown, this)
    });
    return this.subparsers[name].parser;
  }

  parseSubparsers(args) {
    if (Object.keys(this.subparsers).length === 0) {
      if (_.some(args, str => str === '-h' || str === '--help')) return null;
      return undefined;
    }
    for (const cmd in this.subparsers) {
      if (args[0] === this.subparsers[cmd].name ||
          _.some(this.subparsers[cmd].alias, str => str === args[0]))
        return this.subparsers[cmd].parser.parseArgs(_.slice(args, 1));
    }
    if (_.some(args, str => str === '-h' || str === '--help')) {
      return null;
    } else if (this.defaultSubParser) {
      return this.subparsers[this.defaultSubParser].parser.parseArgs(args);
    } else {
      return 'Must specify a subcommand';
    }
  }
  parseArguments(args) {
    if (Object.keys(this.arguments).length === 0) return [args, {}];
    let out = {}
    // Not positional arguments
    for (const optName in this.arguments) {
      const opt = this.arguments[optName];
      if (opt.positional) continue;
      for (const key of opt.names) {
        let idx = -3
        while (idx !== -1) {
          idx = _.indexOf(args, key);
          if (idx === -1) break;
          if (opt.action === 'storeTrue')
            out[opt.dest] = true;
          else if (opt.action === 'storeFalse')
            out[opt.dest] = false;
          else if (opt.action === 'store') {
            if (_.isInteger(opt.nargs) && opt.nargs === 1) {
              out[opt.dest] = opt.type(args[idx + 1]);
              _.pullAt(args, idx, idx + 1);
            } else if (_.isInteger(opt.nargs)) {
              out[opt.dest] = [];
              let j = 0;
              for (i in _.range(opt.nargs)) {
                j = i;
                out[opt.dest].push(opt.type(args[idx + 1 + i]));
              }
              _.pullAt(args, ..._.range(idx, idx + 2 + j));
            } else if (opt.nargs === '?') {
              if (args.length > idx && args[idx + 1][0] !== '-') {
                out[opt.dest] = opt.type(args[idx + 1]);
                _.pullAt(args, idx, idx + 1);
              } else {
                out[opt.dest] = opt.default;
              }
            } else if (opt.nargs === '*') {
              out[opt.dest] = [];
              let i = 0;
              while (args.length > idx + i && args[idx + i][0] !== '-') {
                if (i === 0) continue;
                out[opt.dest].push(opt.type(args[idx + i]));
              }
              _.pullAt(args, ..._.range(idx, idx + i + 1));
            } else if (opt.nargs === '+') {
              out[opt.dest] = [opt.type(args[idx + 1])];
              let i = 1;
              while (args.length > idx + i && args[idx + i][0] !== '-') {
                if (i === 0 || i === 1) continue;
                out[opt.dest].push(opt.type(args[idx + i]));
              }
              _.pullAt(args, _.range(idx, idx + i + 1));
            }
          }
        }
      }
    }
    // Positional arguments
    for (const optName in this.arguments) {
      const opt = this.arguments[optName];
      if (!opt.positional) continue;
      if (_.isInteger(opt.nargs) && opt.nargs === 1) {
        out[opt.dest] = opt.type(args[0]);
        args = _.slice(args, 1);
      } else if (_.isInteger(opt.nargs)) {
        out[opt.dest] = [];
        for (i in _.range(opt.nargs)) {
          out[opt.dest].push(opt.type(args[0]));
          args = _.slice(args, 1);
        }
      } else if (opt.nargs === '?') {
        if (args.length > 0 && args[0][0] !== '-')
          opt[opt.dest] = opt.type(args[0]);
        else
          opt[opt.dest] = opt.type(opt.default);
        args = _.slice(args, 1);
      } else if (opt.nargs === '*') {
        out[opt.dest] = [];
        while (args.length > 0 && args[0][0] !== '-') {
          out[opt.dest].push(opt.type(args[0]));
          args = _.slice(args, 1);
        }
      } else if (opt.nargs === '+') {
        out[opt.dest] = opt.type(args[0]);
        args = _.slice(args, 1);
        while (args.length > 0 && args[0][0] !== '-') {
          out[opt.dest].push(opt.type(args[0]));
          args = _.slice(args, 1);
        }
      }
      if (out[opt.dest] === opt.type(undefined) && opt.required === true) {
        return `Option ${optName} is required`;
      }
    }
    return [args, out];
  }

  parseArgs(args = null) {
    if (args === null) args = _.slice(process.argv, 2);
    let out = {};
    let ret = this.parseSubparsers(args);
    if (ret === null) {
      this.printHelp();
      return undefined;
    } else if (_.isString(ret)) {
      console.error(ret);
      return undefined;
    } else if (ret !== undefined) {
      out = _.merge(out, ret);
    }
    ret = this.parseArguments(args);
    if (_.isString(ret)) {
      console.error(ret);
      return undefined;
    } else {
      out = _.merge(out, ret[1]);
      args = ret[0];
    }
    return out;
  }

  getPath(sep = ' ') {
    if (this.parent !== null) return this.parent.getPath(sep) + sep + this.name;
    return this.name;
  }
  formatArgUsage(src) {
    const arg = this.arguments[src];
    let usage = '';
    if (arg.required === false) usage += '[';
    if (!arg.positional) usage += arg.names[0];
    if (arg.action === 'store') {
      if (_.isInteger(arg.nargs))
        usage += (' ' + arg.metavar).repeat(arg.nargs);
      else if (arg.nargs === '?')
        usage += ` [${arg.metavar}]`;
      else if (arg.nargs === '*')
        usage += ` [${arg.metavar} [${arg.metavar}...]]`;
      else if (arg.nargs === '+')
        usage += ` ${arg.metavar} [${arg.metavar}...]`;
    }
    if (arg.required === false) usage += ']';
    return usage;
  }
  formatUsage() {
    let usage = 'Usage: ' + this.getPath();
    if (Object.keys(this.arguments).length !== 0) {
      for (const arg in this.arguments) {
        usage += ' ' + this.formatArgUsage(arg);
      }
    }
    if (Object.keys(this.subparsers).length !== 0) {
      let cmds = [];
      for (const cmd in this.subparsers) {
        cmds = _.concat(
            cmds, this.subparsers[cmd].alias, this.subparsers[cmd].name);
      }
      usage += ' {'
      for (const i in cmds) {
        usage += cmds[i];
        if (i != cmds.length - 1) usage += ', ';
      }
      usage += '} ...';
    }
    return wrapText(usage, 80, this.getPath().length + 8);
  }
  formatDescription() {
    return (this.description !== null) ? wrapText(this.description, 80, 0) :
                                         null;
  }
  formatArguments() {
    let table = [];
    table.push(['-h, --help', 'Display this help message']);
    for (const arg in this.arguments) {
      table.push(
          [this.formatArgUsage(arg), wrapText(this.arguments[arg].help, 50)]);
    }
    return 'Arguments:\n' + formatTable(table, ['>', '<']);
  }
  formatSubparsers() {
    if (Object.keys(this.subparsers).length === 0) return null;
    let table = [];
    for (const name in this.subparsers) {
      table.push([
        name +
            (this.subparsers[name].alias.length !== 0 ?
                 ', ' + _.join(this.subparsers[name].alias, ', ') :
                 ''),
        name
      ]);
    }
    return 'Subcommands:\n' + formatTable(table, ['>', '<']);
  }
  printHelp() {
    const usage = this.formatUsage();
    const description = this.formatDescription();
    const args = this.formatArguments();
    const subparsers = this.formatSubparsers();
    console.log(usage);
    if (description !== null) console.log('\n' + description);
    if (args !== null) console.log('\n' + args);
    if (subparsers !== null) console.log('\n' + subparsers);
  }
};



var parser = new ArgumentParser(
    'laboris', 'Laboris task manager and time tracker CLI interface');

parser.setDefaultSubparser('user');
let user = parser.addSubparser('user');
user.addSubparser(
        'signin',
        {alias: ['signon', 'login', 'logon'], help: 'Sign in to remote server'})
    .addArgument(
        'email', {required: true, help: 'Email address of user account'})
    .addArgument(
        'password', {required: true, help: 'Password for user account'});
user.addSubparser('signout', {
  alias: ['signoff', 'logout', 'logoff'],
  help: 'Sign out of remote server'
});
user.addSubparser('create', {
      alias: ['register'],
      help: 'Create a new user and sign in to remote server'
    })
    .addArgument(
        'email', {required: true, help: 'Email address of new user account'})
    .addArgument('password', {
      dest: 'password1',
      required: true,
      help: 'Password for new user account'
    })
    .addArgument('password', {
      dest: 'password2',
      required: true,
      help: 'Password for new user account'
    });

parser.addSubparser('config', {help: 'Change configuration variables'})
    .addArgument('value', {required: true, help: 'Value name to reference'})
    .addArgument(
        '-s,--set', {help: 'String value to assign to referenced variable'});


module.exports.parse = () => {
  return parser.parseArgs();
}