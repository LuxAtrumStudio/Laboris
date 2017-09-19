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

   private:
    bool status;
    int priority;
    std::string description;
    std::vector<std::string> tags, projects;
    time_t entry, due, done;
  };
}  // namespace laboris

#endif /* ifndef LABORIS_TASK_HPP */
