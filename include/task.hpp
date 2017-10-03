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
    Task();
    explicit Task(std::string str);
    std::string Print(std::string fmt);

    bool DueToday();
    bool OverDue();

    bool IsInt(std::string str);
    bool IsInt(char ch);

    unsigned int status;
    std::string uuid;
    int priority;
    double urgency;
    std::string description;
    std::vector<std::string> tags, projects;
    // std::vector<Time> times;
    struct tm entry, due, complete;
    bool due_;

   private:
    void GenerateUuid();
    void LoadUrgency();
    std::string GetDateString(std::string str, size_t* i);

    double UrgencyAge();
    double UrgencyDue();
    double UrgencyTags();
    double UrgencyPriority();
    double UrgencyProjects();
  };
}  // namespace laboris

#endif /* ifndef LABORIS_TASK_HPP */
