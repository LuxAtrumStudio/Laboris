// Copyright 2017 Arden Rasmussen
#ifndef LABORIS_CLI_HPP_
#define LABORIS_CLI_HPP_

#include <string>

namespace laboris {
  int GetTaskId(std::string str);
  void AddTask(std::string str);
  void CompleteTask(int id);
  void ParseOptions(int argc, char const* argv[]);

}  // namespace laboris

#endif /* ifndef LABORIS_CLI_HPP_ */
