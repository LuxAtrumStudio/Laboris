// Copyright 2017 Arden Rasmussen
#ifndef LABORIS_CLI_HPP_
#define LABORIS_CLI_HPP_

#include <string>
#include <utility>

#include "task.hpp"

namespace laboris {
  bool IsTaskId(std::string str);
  std::pair<laboris::Task*, int> GetTask(std::string str);

  void AddTask(std::string str);
  void CompleteTask(std::pair<Task*, int> task);
  void DeleteTask(std::pair<Task*, int> task);

  bool ParseCmd(int argc, const char* argv[]);
  bool ParseTaskCmd(int argc, const char* argv[]);
  bool ParseList(int argc, const char* argv[]);
  void ParseOptions(int argc, char const* argv[]);

}  // namespace laboris

#endif /* ifndef LABORIS_CLI_HPP_ */
