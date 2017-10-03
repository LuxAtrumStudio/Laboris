#include "file.hpp"

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "laboris.hpp"
#include "task.hpp"

void laboris::LoadTasks(std::string file) {
  std::ifstream load(file.c_str());
  if (load.is_open()) {
    std::string line;
    while (getline(load, line)) {
      Task new_task(line);
      if (new_task.status == DONE) {
        completed_tasks_.push_back(new_task);
      } else {
        global_tasks_.push_back(new_task);
      }
    }
  } else {
    std::cout << "Could not open file \"" << file << "\"\n";
  }
}

void laboris::SaveTasks(std::string file) {
  std::ofstream save(file.c_str());
  if (save.is_open()) {
    for (size_t i = 0; i < global_tasks_.size(); i++) {
      std::string line = "";
      if (global_tasks_[i].status == DONE) {
        line += "X ";
      }
      line += global_tasks_[i].Print("(%P) ");
      if (global_tasks_[i].status == DONE) {
        line += global_tasks_[i].Print("%C ");
      }
      line += global_tasks_[i].Print("%E %d ");
      for (size_t j = 0; j < global_tasks_[i].tags.size(); j++) {
        line += "@" + global_tasks_[i].tags[j] + " ";
      }
      for (size_t j = 0; j < global_tasks_[i].projects.size(); j++) {
        line += "+" + global_tasks_[i].projects[j] + " ";
      }
      if (global_tasks_[i].due_ == true) {
        line += "due:" + global_tasks_[i].Print("%D") + " ";
      }
      save << line << "\n";
    }
    for (size_t i = 0; i < completed_tasks_.size(); i++) {
      std::string line = "";
      if (completed_tasks_[i].status == DONE) {
        line += "X ";
      }
      line += completed_tasks_[i].Print("(%P) ");
      if (completed_tasks_[i].status == DONE) {
        line += completed_tasks_[i].Print("%C ");
      }
      line += completed_tasks_[i].Print("%E %d ");
      for (size_t j = 0; j < completed_tasks_[i].tags.size(); j++) {
        line += "@" + completed_tasks_[i].tags[j] + " ";
      }
      for (size_t j = 0; j < completed_tasks_[i].projects.size(); j++) {
        line += "+" + completed_tasks_[i].projects[j] + " ";
      }
      if (completed_tasks_[i].due_ == true) {
        line += "due:" + completed_tasks_[i].Print("%D") + " ";
      }
      save << line << "\n";
    }
  }
}
