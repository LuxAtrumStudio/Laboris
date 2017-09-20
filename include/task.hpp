#ifndef LABORIS_TASK_HPP
#define LABORIS_TASK_HPP

#include <time.h>
#include <string>
#include <vector>

namespace laboris {

  enum Status { DONE, PENDING };

  class Task {
   public:
    Task(std::string str);
    std::string Print(std::string fmt);

    bool status;
    int priority;
    std::string description;
    std::vector<std::string> tags, projects;
    // std::vector<Time> times;
    struct tm entry, due, complete;
    // time_t entry, due, done, total;
  };
}  // namespace laboris

#endif /* ifndef LABORIS_TASK_HPP */
