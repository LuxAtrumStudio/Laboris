#ifndef LABORIS_FILE_HPP
#define LABORIS_FILE_HPP

#include "task.hpp"

#include <string>
#include <vector>

namespace laboris {
  void LoadTasks(std::string file);
  void SaveTasks(std::string file);

}  // namespace laboris

#endif /* ifndef LABORIS_FILE_HPP */
