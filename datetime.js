const _ = require('lodash');
const moment = require('moment');

const parseRelativeDate = str => {
  var res = moment();
  Array.from(str.matchAll(/([\+-])(\d*)([wdhms])/gim)).forEach(mod => {
    if (mod[2] === '') mod[2] = '1';
    if (mod[1] === '+')
      res.add({
        weeks: mod[3] === 'w' ? parseInt(mod[2]) : 0,
        days: mod[3] === 'd' ? parseInt(mod[2]) : 0,
        hours: mod[3] === 'h' ? parseInt(mod[2]) : 0,
        minutes: mod[3] === 'm' ? parseInt(mod[2]) : 0,
        seconds: mod[3] === 's' ? parseInt(mod[2]) : 0
      });
    else
      res.subtract({
        weeks: mod[3] === 'w' ? parseInt(mod[2]) : 0,
        days: mod[3] === 'd' ? parseInt(mod[2]) : 0,
        hours: mod[3] === 'h' ? parseInt(mod[2]) : 0,
        minutes: mod[3] === 'm' ? parseInt(mod[2]) : 0,
        seconds: mod[3] === 's' ? parseInt(mod[2]) : 0
      });
  });
  return res.valueOf();
};

module.exports.parse = str => {
  // TODO Error matching 19:06 as 2019-06-02T02:00:00.000Z. It seems to be using
  // the MM-DD format
  if (str === undefined) return undefined;
  if (typeof str === 'number') {
    return str;
  } else if (str.match(/today/i)) {
    return moment().set({hour: 0, minute: 0, second: 0}).valueOf();
  } else if (str.match(/tomorrow/i)) {
    return moment()
        .set({hour: 0, minute: 0, second: 0})
        .add({days: 1})
        .valueOf();
  } else if (str.match(/yesterday/i)) {
    return moment()
        .set({hour: 0, minute: 0, second: 0})
        .subtract({days: 1})
        .valueOf();
  } else if (str.match(/([\+-]\d*[wdhms])+/i))
    return parseRelativeDate(str);

  dateFormats = [
    '', 'DD-MM-YYYY', 'MM-DD-YYYY', 'DD-MM-YY', 'MM-DD-YY', 'DD-MM', 'MM-DD',
    'DD', 'ddd', 'dddd'
  ];

  timeFormats = [
    '', 'hh:mm:ss A', 'hh:mm:ssA', 'hh:mm A', 'hh:mmA', 'hh A', 'hhA',
    'HH:mm:ss', 'HH:mm', 'HH'
  ];

  validFormats = [
    'DD-MM-YYYY',
    'DD-MM-YYYYThh:mm:ss A',
    'DD-MM-YYYYThh:mm:ssA',
    'DD-MM-YYYYThh:mm A',
    'DD-MM-YYYYThh:mmA',
    'DD-MM-YYYYThh A',
    'DD-MM-YYYYThhA',
    'DD-MM-YYYYTHH:mm:ss',
    'DD-MM-YYYYTHH:mm',
    'DD-MM-YYYYTHH',
    'MM-DD-YYYY',
    'MM-DD-YYYYThh:mm:ss A',
    'MM-DD-YYYYThh:mm:ssA',
    'MM-DD-YYYYThh:mm A',
    'MM-DD-YYYYThh:mmA',
    'MM-DD-YYYYThh A',
    'MM-DD-YYYYThhA',
    'MM-DD-YYYYTHH:mm:ss',
    'MM-DD-YYYYTHH:mm',
    'MM-DD-YYYYTHH',
    'DD-MM-YY',
    'DD-MM-YYThh:mm:ss A',
    'DD-MM-YYThh:mm:ssA',
    'DD-MM-YYThh:mmm A',
    'DD-MM-YYThh:mmA',
    'DD-MM-YYThh A',
    'DD-MM-YYThhA',
    'DD-MM-YYTHH:mm:ss',
    'DD-MM-YYTHH:mm',
    'DD-MM-YYTHH',
    'MM-DD-YY',
    'MM-DD-YYThh:mm:ss A',
    'MM-DD-YYThh:mm:ssA',
    'MM-DD-YYThh:mm A',
    'MM-DD-YYThh:mmA',
    'MM-DD-YYThh A',
    'MM-DD-YYThhA',
    'MM-DD-YYTHH:mm:ss',
    'MM-DD-YYTHH:mm',
    'MM-DD-YYTHH',
    'DD-MM',
    'DD-MMThh:mm:ss A',
    'DD-MMThh:mm:ssA',
    'DD-MMThh:mm A',
    'DD-MMThh:mmA',
    'DD-MMThh A',
    'DD-MMThhA',
    'DD-MMTHH:mm:ss',
    'DD-MMTHH:mm',
    'DD-MMTHH',
    'MM-DD',
    'MM-DDThh:mm:ss A',
    'MM-DDThh:mm:ssA',
    'MM-DDThh:mm A',
    'MM-DDThh:mmA',
    'MM-DDThh A',
    'MM-DDThhA',
    'MM-DDTHH:mm:ss',
    'MM-DDTHH:mm',
    'MM-DDTHH',
    'DD',
    'DDThh:mm:ss A',
    'DDThh:mm:ssA',
    'DDThh:mm A',
    'DDThh:mmA',
    'DDThh A',
    'DDThhA',
    'DDTHH:mm:ss',
    'DDTHH:mm',
    'DDTHH',
    'ddd',
    'dddThh:mm:ss A',
    'dddThh:mm:ssA',
    'dddThh:mm A',
    'dddThh:mmA',
    'dddThh A',
    'dddThhA',
    'dddTHH:mm:ss',
    'dddTHH:mm',
    'dddTHH',
    'dddd',
    'ddddThh:mm:ss A',
    'ddddThh:mm:ssA',
    'ddddThh:mm A',
    'ddddThh:mmA',
    'ddddThh A',
    'ddddThhA',
    'ddddTHH:mm:ss',
    'ddddTHH:mm',
    'ddddTHH',
    'hh:mm:ss A',
    'hh:mm:ssA',
    'hh:mm A',
    'hh:mmA',
    'hh A',
    'hhA',
    'HH:mm:ss',
    'HH:mm',
    'HH'
  ];

  const res = moment(str, validFormats);
  if (!res.isValid()) {
    return undefined;
  }
  if (res.valueOf() < _.now() && !str.match(/[0-9]|\s/i))
    return res.add({days: 7}).valueOf();
  return res.valueOf();
};