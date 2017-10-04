#ifndef LABORIS_FILE_HPP
#define LABORIS_FILE_HPP

#include "task.hpp"

#include <string>
#include <vector>

namespace laboris {
  bool IsFile(std::string file);

  void LoadTasks(std::string file);
  void SaveTasks(std::string file);

}  // namespace laboris

#endif /* ifndef LABORIS_FILE_HPP */
