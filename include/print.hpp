#ifndef LABORIS_PRINT_HPP
#define LABORIS_PRINT_HPP

#include "task.hpp"

namespace laboris {
  void PrintTasks(unsigned int s);
  void PrintDetails(int id);
  void PrintAction(std::vector<std::string> data, std::vector<int> colors);
}  // namespace laboris

#endif /* ifndef LABORIS_PRINT_HPP */
