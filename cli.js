const _ = require('lodash');
const chalk = require('chalk');
const Conf = require('conf');
const envPaths = require('env-paths');
const fs = require('fs');

const paths = envPaths('Laboris', {suffix: ''});
const config = new Conf({
  'projectSuffix': '',
  'serialize': value => JSON.stringify(value, null, '  '),
  defaults: {
    'remoteUrl': 'https://laboris.luxater.com/',
    'dataFile': `${paths.data}/data.json`,
    'modifiedFile': `${paths.data}/modified.json`,
    'cli': {
      'error': ['bold', 'red'],
      'note': ['bold', 'cyan'],
      'success': ['bold', 'green']
    }
  }
});

const defaultColors = [
  'black',          'red',           'green',
  'yellow',         'blue',          'magenta',
  'cyan',           'white',         'blackBright',
  'redBright',      'greenBright',   'yellowBright',
  'blueBright',     'magentaBright', 'cyanBright',
  'whiteBright',    'bgBlack',       'bgRed',
  'bgGreen',        'bgYellow',      'bgBlue',
  'bgMagenta',      'bgCyan',        'bgWhite',
  'bgBlackBright',  'bgRedBright',   'bgGreenBright',
  'bgYellowBright', 'bgBlueBright',  'bgagentaBright',
  'bgCyanBright',   'bgWhiteBright',
];
const defaultModifiers = [
  'reset', 'bold', 'dim', 'italic', 'underline', 'inverse', 'hidden',
  'strikethough', 'visible'
];


module.exports.config = {};
module.exports.config.get = str => {
  return config.get(str);
};
module.exports.config.has = str => {
  return config.has(str);
};
module.exports.config.set = (str, val = undefined) => {
  return config.set(str, val);
};

module.exports.local = {};
module.exports.local.loadFile = (file) => {
  return new Promise((resolve, reject) => {
           fs.exists(file, (err, data) => {
             if (err)
               reject(err);
             else
               resolve(data);
           });
         })
      .then(data => {
        return new Promise((resolve, reject) => {
          if (data) {
            fs.readFile(file, 'utf8', (err, data) => {
              if (err)
                reject(err);
              else
                resolve(JSON.parse(data));
            });
          } else {
            resolve({});
          }
        });
      });
};
module.exports.local.saveFile = (file, data) => {
  return new Promise((resolve, reject) => {
    fs.writeFile(file, JSON.stringify(data), (err) => {
      if (err)
        reject(err);
      else
        resolve();
    });
  });
};
module.exports.local.load = () => {
  return this.local.loadFile(config.get('dataFile'));
};
module.exports.local.loadModified = () => {
  return this.local.loadFile(config.get('modifiedFile'));
};
module.exports.local.save = (data) => {
  return this.local.saveFile(config.get('dataFile'), data);
};
module.exports.local.saveModified = (data) => {
  return this.local.saveFile(config.get('modifiedFile'), data);
};

module.exports.getDisplayFormat = (ref, base = chalk) => {
  if (ref === undefined || ref == null) return base;
  if (_.isArray(ref)) {
    let color = base;
    for (const colorSpec of ref) {
      color = this.getDisplayFormat(colorSpec, color);
    }
    return color;
  } else if (defaultColors.includes(ref)) {
    if (ref === 'black')
      return base.black;
    else if (ref === 'red')
      return base.red;
    else if (ref === 'green')
      return base.green;
    else if (ref === 'yellow')
      return base.yellow;
    else if (ref === 'blue')
      return base.blue;
    else if (ref === 'magenta')
      return base.magenta;
    else if (ref === 'cyan')
      return base.cyan;
    else if (ref === 'white')
      return base.white;
    else if (ref === 'blackBright')
      return base.blackBright;
    else if (ref === 'redBright')
      return base.redBright;
    else if (ref === 'greenBright')
      return base.greenBright;
    else if (ref === 'yellowBright')
      return base.yellowBright;
    else if (ref === 'blueBright')
      return base.blueBright;
    else if (ref === 'magentaBright')
      return base.magentaBright;
    else if (ref === 'cyanBright')
      return base.cyanBright;
    else if (ref === 'whiteBright')
      return base.whiteBright;
    else if (ref === 'bgBlack')
      return base.bgBlack;
    else if (ref === 'bgEed')
      return base.bgRed;
    else if (ref === 'bgGreen')
      return base.bgGreen;
    else if (ref === 'bgYellow')
      return base.bgYellow;
    else if (ref === 'bgBlue')
      return base.bgBlue;
    else if (ref === 'bgMagenta')
      return base.bgMagenta;
    else if (ref === 'bgCyan')
      return base.bgCyan;
    else if (ref === 'bgWhite')
      return base.bgWhite;
    else if (ref === 'bgBlackBright')
      return base.bgBlackBright;
    else if (ref === 'bgRedBright')
      return base.bgRedBright;
    else if (ref === 'bgGreenBright')
      return base.bgGreenBright;
    else if (ref === 'bgYellowBright')
      return base.bgYellowBright;
    else if (ref === 'bgBlueBright')
      return base.bgBlueBright;
    else if (ref === 'bgMagentaBright')
      return base.bgMagentaBright;
    else if (ref === 'bgCyanBright')
      return base.bgCyanBright;
    else if (ref === 'bgWhiteBright')
      return base.bgWhiteBright;
  } else if (defaultModifiers.includes(ref)) {
    if (ref === 'reset')
      return base.reset;
    else if (ref === 'bold')
      return base.bold;
    else if (ref === 'dim')
      return base.dim;
    else if (ref === 'italic')
      return base.italic;
    else if (ref === 'underline')
      return base.underline;
    else if (ref === 'inverse')
      return base.inverse;
    else if (ref === 'hidden')
      return base.hidden;
    else if (ref === 'strikethrough')
      return base.strikethrough;
    else if (ref === 'visible')
      return base.visible;
  } else if (ref[0] !== '#') {
    return base.keyword(ref);
  } else {
    return chalk.hex(hex);
  }
};

module.exports.printMsg = (msg, color = chalk.default, indent = 0) => {
  console.log(color(' '.repeat(indent) + msg));
};
module.exports.printError = (err, indent = 0) => {
  this.printMsg(
      err, this.getDisplayFormat(this.config.get('cli.error')), indent);
};
module.exports.printNote = (err, indent = 0) => {
  this.printMsg(
      err, this.getDisplayFormat(this.config.get('cli.note')), indent);
};
module.exports.printSuccess = (err, indent = 0) => {
  this.printMsg(
      err, this.getDisplayFormat(this.config.get('cli.success')), indent);
};

module.exports.displayLength = (msg) => {
  let len = 0;
  let state = 0;
  for (const char of msg) {
    if (char == '\u001b')
      state = 1;
    else if (state == 1 && char == 'm')
      state = 0;
    else if (state == 0)
      len += 1;
  }
  return len;
};

module.exports.wrapText = (str, width = 80, indent = 2, initIndent = 0) => {
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

module.exports.alignLeft = (str, len, char = ' ') => {
  return str + char.repeat(Math.max(len - this.displayLength(str), 0));
};
module.exports.alignRight = (str, len, char = ' ') => {
  return char.repeat(Math.max(len - this.displayLength(str), 0)) + str;
};
module.exports.alignCenter = (str, len, char = ' ') => {
  return char.repeat(
             Math.max(Math.floor(len - this.displayLength(str) / 2), 0)) +
      str +
      char.repeat(Math.max(Math.ceil(len - this.displayLength(str) / 2), 0));
};

module.exports.printTable = (table, zebra = false, alignment = []) => {
  let colWidth = [];
  for (const r in table) {
    for (const c in table[r]) {
      if (c >= colWidth.length)
        colWidth.push(this.displayLength(table[r][c]));
      else
        colWidth[c] = Math.max(colWidth[c], this.displayLength(table[r][c]));
    }
  }
  if (alignment.length === 0) alignment = [this.alignLeft] * colWidth.length;
  for (const r in table) {
    let line = '';
    for (const c in table[r]) {
      if (c !== 0) line += '  ';
      line += alignment[c](table[r][c], colWidth[c]);
    }
    if (zebra && r % 2 == 0)
      console.log(chalk.bgBlack(line));
    else
      console.log(line);
  }
}