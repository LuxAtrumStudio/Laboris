module.exports.start = (args) => {

}
module.exports.startHelp = () => {
  return {
    usage: "start REF [TIME]",
    'ref': "Reference to a task utilizing any of the referencing parameters",
    "time": "Start time of the task, using the standard date/time parameter options."
  };
}
