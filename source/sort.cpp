#include "sort.hpp"

#include <algorithm>
#include <vector>

#include <iostream>

#include "laboris.hpp"
#include "task.hpp"

bool laboris::IDSort(const Task& lhs, const Task& rhs) {
  return lhs.id < rhs.id;
}
bool laboris::ProjectSort(const Task& lhs, const Task& rhs) {
  std::string lhs_s = lhs.Print("%p*");
  std::string rhs_s = rhs.Print("%p*");
  if (lhs_s == "" && rhs_s != "") {
    return false;
  }
  return lhs_s < rhs_s;
}
bool laboris::TagSort(const Task& lhs, const Task& rhs) {
  std::string lhs_s = lhs.Print("%t*");
  std::string rhs_s = rhs.Print("%t*");
  if (lhs_s == "" && rhs_s != "") {
    return false;
  }
  return lhs_s > rhs_s;
}
bool laboris::DescriptionSort(const Task& lhs, const Task& rhs) {
  return lhs.description < rhs.description;
}
bool laboris::CompletedSort(const Task& lhs, const Task& rhs) {
  if (lhs.status != DONE && rhs.status == DONE) {
    return false;
  }
  return lhs.complete_time < rhs.complete_time;
}
bool laboris::EnteredSort(const Task& lhs, const Task& rhs) {
  return lhs.entry_time < rhs.entry_time;
}
bool laboris::DueSort(const Task& lhs, const Task& rhs) {
  if (lhs.due_ == false && rhs.due_ == true) {
    return false;
  }
  return lhs.due_time < rhs.due_time;
}
bool laboris::PrioritySort(const Task& lhs, const Task& rhs) {
  return lhs.priority < rhs.priority;
}
bool laboris::UrgencySort(const Task& lhs, const Task& rhs) {
  return lhs.urgency > rhs.urgency;
}

void laboris::SortTasks(unsigned int method, bool inverse, unsigned int s) {
  std::vector<laboris::Task>::iterator begin, end;
  if (s == 0) {
    begin = global_tasks_.begin();
    end = global_tasks_.end();
  } else if (s == 1) {
    begin = completed_tasks_.begin();
    end = completed_tasks_.end();
  }
  if (s == 0) {
    if (method == SORT_ID) {
      std::sort(begin, end, IDSort);
    } else if (method == SORT_PROJECT) {
      std::sort(begin, end, ProjectSort);
    } else if (method == SORT_TAGS) {
      std::sort(begin, end, TagSort);
    } else if (method == SORT_DESCRIPTION) {
      std::sort(begin, end, DescriptionSort);
    } else if (method == SORT_COMPLETED) {
      std::sort(begin, end, CompletedSort);
    } else if (method == SORT_ENTERED) {
      std::sort(begin, end, EnteredSort);
    } else if (method == SORT_DUE) {
      std::sort(begin, end, DueSort);
    } else if (method == SORT_PRIORITY) {
      std::sort(begin, end, PrioritySort);
    } else if (method == SORT_URGENCY) {
      std::sort(begin, end, UrgencySort);
    }
  }
}
