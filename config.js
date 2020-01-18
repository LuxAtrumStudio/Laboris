const _ = require('lodash');
const Conf = require('conf');
const envPaths = require('env-paths');
const tinygradient = require('tinygradient');

const paths = envPaths('laboris', {suffix: ''});
const config = new Conf({
  projectName: 'laboris',
  projectSuffix: '',
  serialize: (value) => JSON.stringify(value),
  defaults: {
    dataFile: paths.data + '/data.json',
    configFile: paths.config + '/config.json',
    ...require('./defaultConfig.json'),
  },
});
module.exports = config;
const configureColor = (base) => {
  const baseColors = config.get('colors');
  const baseKeys = Object.keys(baseColors);
  if (base.fg === undefined) base.fs = '';
  if (base.bg === undefined) base.bg = '';
  if (base.attr === undefined) base.attr = [];
  for (const baseKey of baseKeys) {
    base.fg =
        base.fg.replace(new RegExp('{' + baseKey + '}'), baseColors[baseKey]);
    base.bg =
        base.bg.replace(new RegExp('{' + baseKey + '}'), baseColors[baseKey]);
  }
  return base;
};
module.exports.getColor = (key) => {
  const baseColors = config.get('colors');
  const baseKeys = Object.keys(baseColors);
  if (key in baseColors) return {fg: baseColors[key], bg: '', attr: []};
  return configureColor(config.get(key));
};
module.exports.getUrgColor = (urg) => {
  const urgGradient = _.map(config.get('urgGradient'), configureColor);
  const fgGradient = _.map(urgGradient, (c) => {
    return {color: c.fg, pos: c.pos};
  });
  const bgGradient = _.map(urgGradient, (c) => {
    return {color: c.bg, pos: c.pos};
  });
  const pos = _.clamp(urg / 10.0, 0, 1);
  let attr = [];
  for (const level of urgGradient) {
    if (level.pos <= pos) attr = level.attr !== undefined ? level.attr : [];
  }
  return {fg: tinygradient(fgGradient).hsvAt(pos), bg: '', attr};
};
