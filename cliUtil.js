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
  console.log(res);
};

module.exports.printTable = (table, alignment = []) => {
  let colWidth = [];
  for (const r in table) {
    for (const c in table[r]) {
      if (c >= colWidth.length)
        colWidth.push(table[r][c].length);
      else
        colWidth[c] = Math.max(colWidth[c], table[r][c].length);
    }
  }
  while (alignment.length < colWidth.length) {
    alignment.push('<');
  }
  for (const r in table) {
    let line = '';
    for (const c in table[r]) {
      if (c !== 0) line += '  ';
      if (alignment[c] === '<')
        line += table[r][c].padEnd(colWidth[c]);
      else if (alignment[c] === '>')
        line += table[r][c].padStart(colWidth[c]);
    }
    console.log(line);
  }
};