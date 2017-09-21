#include "load.hpp"

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "task.hpp"

std::vector<laboris::Task> laboris::LoadTasks(std::string file) {
  std::vector<Task> tasks;
  std::ifstream load(file.c_str());
  if (load.is_open()) {
    std::string line;
    while (getline(load, line)) {
      tasks.push_back(line);
    }
  } else {
    std::cout << "Could not open file \"" << file << "\"\n";
  }
  return tasks;
}
