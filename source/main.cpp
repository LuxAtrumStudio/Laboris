#include "laboris.hpp"

#include <iostream>
#include <vector>

int main(int argc, char const* argv[]) {
  laboris::LoadTasks("todo.txt");
  laboris::ParseOptions(argc, argv);
  laboris::SaveTasks("todo.txt");
  return 0;
}
