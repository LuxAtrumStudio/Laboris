#ifndef LABORIS_LOAD_HPP
#define LABORIS_LOAD_HPP

#include "task.hpp"

#include <string>
#include <vector>

namespace laboris {
  std::vector<Task> LoadTasks(std::string file);
}  // namespace laboris

#endif /* ifndef LABORIS_LOAD_HPP */
