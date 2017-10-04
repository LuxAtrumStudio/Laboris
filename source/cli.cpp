// Copyright 2017 Arden Rasmussen
#include "cli.hpp"

#include <stdio.h>
#include <iostream>
#include <string>

#include "laboris.hpp"
#include "output.hpp"
#include "task.hpp"

bool laboris::IsTaskId(std::string str) {
  for (int i = 0; i < global_tasks_.size(); i++) {
    if (global_tasks_[i].uuid == str ||
        std::to_string(global_tasks_[i].id) == str) {
      return true;
    }
  }
  for (int i = 0; i < completed_tasks_.size(); i++) {
    if (completed_tasks_[i].uuid == str) {
      return true;
    }
  }
  return false;
}

std::pair<laboris::Task*, int> laboris::GetTask(std::string str) {
  for (int i = 0; i < global_tasks_.size(); i++) {
    if (global_tasks_[i].uuid == str) {
      return {&global_tasks_[i], global_tasks_[i].id};
    } else if (std::to_string(global_tasks_[i].id) == str) {
      return {&global_tasks_[i], global_tasks_[i].id};
    }
  }
  for (int i = 0; i < completed_tasks_.size(); i++) {
    if (completed_tasks_[i].uuid == str) {
      return {&completed_tasks_[i], i};
    }
  }
}

void laboris::AddTask(std::string str) {
  Task new_task(str);
  time_t current = time(NULL);
  new_task.entry = *localtime(&current);
  new_task.id = global_tasks_.size();
  global_tasks_.push_back(new_task);
  PrintAction({"Added Task " + std::to_string(new_task.id),
               {"  \'" + new_task.Print("%d") + "\'"}},
              {cli::GREEN});
}

void laboris::CompleteTask(std::pair<Task*, int> task) {
  if (task.first->status != DONE) {
    task.first->status = DONE;
    PrintAction({"Completed Task " + std::to_string(task.second),
                 "  \'" + task.first->Print("%d") + "\'"},
                {cli::YELLOW});
    completed_tasks_.push_back(global_tasks_[task.second]);
    global_tasks_.erase(global_tasks_.begin() + task.second);
  }
}

void laboris::DeleteTask(std::pair<Task*, int> task) {
  PrintAction({"Deleted Task " + std::to_string(task.second),
               "  \'" + task.first->Print("%d") + "\'"},
              {cli::RED});
  if (task.first->status == DONE) {
    completed_tasks_.erase(completed_tasks_.begin() + task.second);
  } else {
    global_tasks_.erase(global_tasks_.begin() + task.second);
  }
}

bool laboris::ParseCmd(int argc, const char* argv[]) {
  if (std::string(argv[1]) == "add") {
    std::string task_str;
    for (int i = 2; i < argc; i++) {
      task_str += argv[i];
      task_str += ' ';
    }
    AddTask(task_str);
    return true;
  }
  return false;
}

bool laboris::ParseTaskCmd(int argc, const char* argv[]) {
  if (IsTaskId(argv[1]) == true) {
    if (argc == 2) {
      PrintDetails(GetTask(argv[1]).first);
      return true;
    } else {
      if (std::string(argv[2]) == "done") {
        CompleteTask(GetTask(argv[1]));
        return true;
      } else if (std::string(argv[2]) == "delete") {
        DeleteTask(GetTask(argv[1]));
        return true;
      }
    }
  }
  return false;
}

bool laboris::ParseList(int argc, const char* argv[]) {
  int s = -1, method = SORT_URGENCY;
  bool err = false;
  for (int i = 1; i < argc; i++) {
    if (s == -1 && std::string(argv[i]) == "all") {
      s = 2;
    } else if (s == -1 && std::string(argv[i]) == "complete") {
      s = 1;
    } else if (s == -1 && std::string(argv[i]) == "pending") {
      s = 0;
    } else if (std::string(argv[i]) == "id") {
      method = SORT_ID;
    } else if (std::string(argv[i]) == "project") {
      method = SORT_PROJECT;
    } else if (std::string(argv[i]) == "tag") {
      method = SORT_TAGS;
    } else if (std::string(argv[i]) == "description") {
      method = SORT_DESCRIPTION;
    } else if (std::string(argv[i]) == "enter") {
      method = SORT_ENTERED;
    } else if (std::string(argv[i]) == "due") {
      method = SORT_DUE;
    } else if (std::string(argv[i]) == "done") {
      method = SORT_COMPLETED;
    } else if (std::string(argv[i]) == "priority") {
      method = SORT_PRIORITY;
    } else if (std::string(argv[i]) == "urgency") {
      method = SORT_URGENCY;
    } else {
      err = true;
      std::cout << cli::Bold(
          cli::Red("Unknown command \'" + std::string(argv[i]) + "\'\n"));
    }
  }
  if (s == -1) {
    s = 0;
  }
  if (err == false) {
    PrintTasks(s, method);
  }
  return true;
}

void laboris::ParseOptions(int argc, char const* argv[]) {
  unsigned int s = 0, method = SORT_URGENCY;
  if (argc == 1) {
    PrintTasks(0, SORT_URGENCY);
    return;
  }
  if (ParseCmd(argc, argv) == true) {
    return;
  }
  if (ParseTaskCmd(argc, argv) == true) {
    return;
  }
  if (ParseList(argc, argv) == true) {
    return;
  }
  printf(cli::Red("Unknown command \'%s\'\n").c_str(), argv[1]);
}
