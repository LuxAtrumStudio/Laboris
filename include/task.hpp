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

    unsigned int status;
    unsigned int uuid;
    int priority;
    double urgency;
    std::string description;
    std::vector<std::string> tags, projects;
    // std::vector<Time> times;
    struct tm entry, due, complete;

   private:
    void GenerateUuid();
    void LoadUrgency();
    std::string GetDateString(std::string str, int& i);

    bool due_;
  };
}  // namespace laboris

#endif /* ifndef LABORIS_TASK_HPP */
