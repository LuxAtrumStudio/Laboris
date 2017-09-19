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
}
