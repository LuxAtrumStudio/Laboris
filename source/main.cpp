#include "task.hpp"

#include <iostream>

int main(int argc, char const* argv[]) {
  laboris::Task task(
      "(5) +MAR 2017-09-08 2017-09-08T15:27:15 This is a test task "
      "+Programming "
      "+Laboris "
      "@Testing "
      "@Arden due:2017-09-19T22:00:00");
  // std::cout << task.Print("Entry: %E\nEnd: %C\nDue: %D") << "\n";
  std::cout << task.Print(
      "%s (%P) %C{%Y-%m-%dT%H:%M:%S} %E{%Y-%m-%dT%H:%M:%S} \"%d\" %t* %p* "
      "due:%D{%Y-%m-%dT%H:%M:%S}\n");
  /* code */
  return 0;
}
