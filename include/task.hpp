// Copyright 2017 Arden Rasmussen

#ifndef LABORIS_TASK_HPP_
#define LABORIS_TASK_HPP_

#include <time.h>
#include <string>
#include <vector>

namespace laboris {

  enum Status { DEF, DONE, PENDING };

  class Task {
   public:
    explicit Task(std::string str);
    std::string Print(std::string fmt);

    bool DueToday();
    bool OverDue();

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
    std::string GetDateString(std::string str, size_t& i);

    double UrgencyAge();
    double UrgencyDue();
    double UrgencyTags();
    double UrgencyPriority();
    double UrgencyProjects();

    bool due_;
  };
}  // namespace laboris

#endif /* ifndef LABORIS_TASK_HPP */
