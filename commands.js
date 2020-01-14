const _ = require('lodash');
const axios = require('axios');
const uuidv5 = require('uuid/v5');

const hasConnection = () => {
  return true;
};

module.exports.user = {};
module.exports.user.signin = (config, args) => {
  if (!hasConnection)
    return new Promise(
      (_resolve,
        reject) => {
        reject({
          error: 'Internet connection must be active to signin'
        })
      });
  return axios
    .post(
      config.get('remoteUrl') + 'user/signin/', {
        email: args.email,
        password: args.password
      })
    .then(response => {
      return new Promise((resolve, reject) => {
        if (response.data.error !== undefined)
          return reject(response.data.error);
        if (response.data.uuid !== undefined)
          config.set('userUuid', response.data.uuid);
        return resolve(response.data);
      });
    });
};
module.exports.user.signout = (config, _args) => {
  return new Promise((resolve, _reject) => {
    if (config.has('userUuid')) {
      config.delete('userUuid');
      resolve({
        success: 'Signed out of current user'
      });
    } else {
      resolve({
        warning: 'Not currently active user'
      });
    }
  });
};
module.exports.user.create = (config, args) => {
  if (!hasConnection)
    return new Promise(
      (_resolve, reject) => {
        reject({
          error: 'Internet connection must be active to create a user'
        })
      });
  if (args.password1 !== args.password2)
    return new Promise(
      (_resolve, reject) => {
        reject('Passwords do not match')
      });
  return axios
    .post(
      config.get('remoteUrl') + 'user/create/', {
        email: args.email,
        password: args.password1
      })
    .then(response => {
      return new Promise((resolve, reject) => {
        if (response.data.uuid !== undefined)
          config.set('userUuid', response.data.uuid);
        return resolve(response.data);
      });
    });
};

module.exports.create = (config, local, args) => {
  return local.load()
    .then(data => {
      let task = _.defaults(args, {
        args.title = _.joint(args.title);
        uuid: uuidv5(_.join(args.title) + _.now().toString(), uuidv5.URL),
        title: '',
        entryDate: _.now(),
        dueDate: null,
        doneDate: null,
        times: [],
        hidden: false,
        open: true,
        parents: [],
        children: [],
        tags: [],
        priority: 5,
        users: [config.has('userUuid') ? config.get('userUuid') : undefined],
        syncTime: _.now()
      });
      return Promise.all([
        new Promise(resolve => resolve(task)),
        local.selectUuids(task.parents), local.selectUuids(task.children)
      ])
    })
    .then(([task, parents, children]) => {
      task.parents = parents;
      task.children = children;
      local.data[task.uuid] = task;
      return Promise.all([
        new Promise(resolve => resolve(task)),
        local.save(), remote.sync(task)
      ]);
    })
    .then(([task, _tmp]) => {
      cli.printSuccess('Created New Task');
      console.log('  ' + cli.formatTask(task));
      return undefined;
    });
};
