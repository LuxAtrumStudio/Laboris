#include "task.hpp"

#include <time.h>
#include <string>
#include <vector>

#include "regex.hpp"

laboris::Task::Task(std::string str) {
  if (str.size() == 0) {
    return;
  }
  if (str[0] == 'x' || str[0] == 'X') {
    status = DONE;
  }
  std::string regex = cli::GenerateDateRegex("%d-%m-%Y%(T%H:%M%(:%S%)%?%)%?");
  std::cout << "regex:" << regex << "\n";
  std::vector<std::string> date_blocks = cli::RegexFind(
      str, cli::GenerateDateRegex("%d-%m-%Y%(T%H:%M%(:%S%)%?%)%?"));
  tags = cli::RegexFind(str, "@[^\\s]+");
  projects = cli::RegexFind(str, "\\+[^\\s]+");
  std::vector<std::string> results = cli::RegexFind(str, "\\(\\d\\)");

  if (results.size() < 1) {
    priority = 0;
  } else {
    priority = int(results[0][1]) - 48;
  }
  std::cout << priority << "\n";

  for (int i = 0; i < date_blocks.size(); i++) {
    std::cout << date_blocks[i] << ",";
  }
  std::cout << "\n";
  for (int i = 0; i < tags.size(); i++) {
    std::cout << tags[i] << ",";
  }
  std::cout << "\n";
  for (int i = 0; i < projects.size(); i++) {
    std::cout << projects[i] << ",";
  }
  std::cout << "\n";
}
