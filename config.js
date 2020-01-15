const Conf = require('conf');
const envPaths = require('env-paths');

module.exports.paths = envPaths('Laboris', {suffix: ''});
module.exports = new Conf('Laboris', {
  projectSuffix: '',
  serialse: value => JSON.stringify(value),
  defaults: {
    dataFile: this.paths.data + '/data.json',
    configFile: this.paths.config + '/config.json',
    ...require('defaultConfig.json')
  }
});
