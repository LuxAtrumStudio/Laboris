// Copyright 2017 Arden Rasmussen
#include "cli.hpp"

#include <stdio.h>
#include <string>

#include "laboris.hpp"
#include "output.hpp"
#include "task.hpp"

bool laboris::IsTaskId(std::string str) {
  bool is_int = true;
  for (size_t i = 0; i < str.size() && is_int == true; i++) {
    if (str[i] > 57 || str[i] < 48) {
      is_int = false;
    }
  }
  if (is_int == true && stoi(str) <= global_tasks_.size() && stoi(str) > 0) {
    return true;
  }
  if (is_int == false) {
    for (int i = 0; i < global_tasks_.size(); i++) {
      if (global_tasks_[i].uuid == str) {
        return true;
      }
    }
    for (int i = 0; i < completed_tasks_.size(); i++) {
      if (completed_tasks_[i].uuid == str) {
        return true;
      }
    }
  }
  return false;
}

std::pair<laboris::Task*, int> laboris::GetTask(std::string str) {
  bool is_int = true;
  for (size_t i = 0; i < str.size() && is_int == true; i++) {
    if (str[i] > 57 || str[i] < 48) {
      is_int = false;
    }
  }
  if (is_int == true && stoi(str) <= global_tasks_.size() && stoi(str) > 0) {
    return {&global_tasks_[stoi(str) - 1], stoi(str) - 1};
  }
  if (is_int == false) {
    for (int i = 0; i < global_tasks_.size(); i++) {
      if (global_tasks_[i].uuid == str) {
        return {&global_tasks_[i], i};
      }
    }
    for (int i = 0; i < completed_tasks_.size(); i++) {
      if (completed_tasks_[i].uuid == str) {
        return {&completed_tasks_[i], i};
      }
    }
  }
}

void laboris::AddTask(std::string str) {
  Task new_task(str);
  time_t current = time(NULL);
  new_task.entry = *localtime(&current);
  global_tasks_.push_back(new_task);
}

void laboris::CompleteTask(std::pair<Task*, int> task) {
  if (task.first->status != DONE) {
    task.first->status = DONE;
    PrintAction({"Completed Task " + std::to_string(task.second),
                 "  \'" + task.first->Print("%d") + "\'"},
                {cli::GREEN});
    completed_tasks_.push_back(global_tasks_[task.second]);
    global_tasks_.erase(global_tasks_.begin() + task.second);
  }
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
  } else if (IsTaskId(argv[1]) == true) {
    if (argc == 2) {
      PrintDetails(GetTask(argv[1]));
    } else {
      if (std::string(argv[2]) == "done") {
        CompleteTask(GetTask(argv[1]));
      }
    }
  }
}
