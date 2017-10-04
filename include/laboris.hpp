#ifndef LABORIS_LABORIS_HPP_
#define LABORIS_LABORIS_HPP_

#include "cli.hpp"
#include "file.hpp"
#include "print.hpp"
#include "sort.hpp"
#include "task.hpp"
#include "time.hpp"

#include <vector>

namespace laboris {
  extern std::vector<Task> global_tasks_, completed_tasks_, tmp_task_list_;
}  // namespace laboris

#endif /* ifndef LABORIS_LABORIS_HPP_ */
