#include "load.hpp"
#include "print.hpp"
#include "task.hpp"

#include <iostream>
#include <vector>

int main(int argc, char const* argv[]) {
  std::vector<laboris::Task> tasks = laboris::LoadTasks("todo.txt");
  laboris::PrintTasks(tasks);
  // for (int i = 0; i < tasks.size(); i++) {
  // std::cout << i + 1 << " " << tasks[i].Print("%d") << "\n";
  // }
  /* code */
  return 0;
}
