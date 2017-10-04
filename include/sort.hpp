#ifndef LABORIS_SORT_HPP
#define LABORIS_SORT_HPP

#include "task.hpp"

namespace laboris {
  enum SortMethod {
    SORT_ID,
    SORT_PROJECT,
    SORT_TAGS,
    SORT_DESCRIPTION,
    SORT_COMPLETED,
    SORT_ENTERED,
    SORT_DUE,
    SORT_PRIORITY,
    SORT_URGENCY
  };
  bool IDSort(const Task& lhs, const Task& rhs);
  bool ProjectSort(const Task& lhs, const Task& rhs);
  bool TagSort(const Task& lhs, const Task& rhs);
  bool DescriptionSort(const Task& lhs, const Task& rhs);
  bool CompletedSort(const Task& lhs, const Task& rhs);
  bool EnteredSort(const Task& lhs, const Task& rhs);
  bool DueSort(const Task& lhs, const Task& rhs);
  bool PrioritySort(const Task& lhs, const Task& rhs);
  bool UrgencySort(const Task& lhs, const Task& rhs);
  void SortTasks(unsigned int method, bool invers, unsigned int s);

}  // namespace laboris

#endif /* ifndef LABORIS_SORT_HPP */
