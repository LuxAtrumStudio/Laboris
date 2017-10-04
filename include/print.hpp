#ifndef LABORIS_PRINT_HPP
#define LABORIS_PRINT_HPP

#include <utility>
#include <vector>

#include "task.hpp"

namespace laboris {
  void PrintTasks(unsigned int s, unsigned int sort_method);
  void PrintDetails(Task* task);
  void PrintAction(std::vector<std::string> data, std::vector<int> colors);
}  // namespace laboris

#endif /* ifndef LABORIS_PRINT_HPP */
