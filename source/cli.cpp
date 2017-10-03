// Copyright 2017 Arden Rasmussen
#include "cli.hpp"

#include <stdio.h>
#include <string>

#include "laboris.hpp"
#include "output.hpp"
#include "task.hpp"

int laboris::GetTaskId(std::string str) {
  bool is_int = true;
  int id = 0;
  for (size_t i = 0; i < str.size() && is_int == true; i++) {
    if (str[i] > 57 || str[i] < 48) {
      is_int = false;
    }
  }
  if (is_int == true) {
    id = stoi(str);
  }
  if (id > global_tasks_.size() || id <= 0) {
    id = 0;
  }
  return (id - 1);
}

void laboris::AddTask(std::string str) {
  Task new_task(str);
  time_t current = time(NULL);
  new_task.entry = *localtime(&current);
  global_tasks_.push_back(new_task);
}

void laboris::CompleteTask(int id) {
  global_tasks_[id].status = DONE;
  completed_tasks_.push_back(global_tasks_[id]);
  global_tasks_.erase(global_tasks_.begin() + id);
  PrintAction({"Completed Task " + std::to_string(id + 1),
               "  \'" + global_tasks_[id].Print("%d") + "\'"},
              {cli::GREEN});
}
void laboris::ParseOptions(int argc, char const* argv[]) {
  if (argc == 1) {
    PrintTasks(0);
    return;
  }
  if (std::string(argv[1]) == "add") {
    std::string task_str;
    for (int i = 2; i < argc; i++) {
      task_str += argv[i];
      task_str += ' ';
    }
    AddTask(task_str);
  } else if (std::string(argv[1]) == "all") {
    PrintTasks(2);
  } else if (std::string(argv[1]) == "completed") {
    PrintTasks(1);
  } else if (GetTaskId(argv[1]) != -1) {
    if (argc == 2) {
      PrintDetails(GetTaskId(argv[1]));
    } else {
      if (std::string(argv[2]) == "done") {
        CompleteTask(GetTaskId(argv[1]));
      }
    }
  }
}
