#include "task.hpp"

#include <time.h>
#include <string>
#include <vector>

#include "regex.hpp"

namespace laboris {
  void LoadTm(std::string date, struct tm* t) {
    if (cli::Regex(date, cli::GenerateDateRegex("%Y-%m-%dT%H:%M:%S")) == true) {
      strptime(date.c_str(), "%y-%m-%dT%H:%M:%S", t);
    } else if (cli::Regex(date, cli::GenerateDateRegex("%Y-%m-%dT%H:%M")) ==
               true) {
      strptime(date.c_str(), "%y-%m-%dT%H:%M", t);
    } else if (cli::Regex(date, cli::GenerateDateRegex("%Y-%m-%d")) == true) {
      strptime(date.c_str(), "%y-%m-%d", t);
    }
  }
}  // namespace laboris

laboris::Task::Task(std::string str) {
  if (str.size() == 0) {
    return;
  }
  if (str[0] == 'x' || str[0] == 'X') {
    status = DONE;
  }
  std::string date_regex =
      "[:blank:]" + cli::GenerateDateRegex("%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?");
  std::cout << date_regex << "<<\n";
  std::vector<std::string> date_blocks = cli::RegexFind(
      str,
      "[:blank:]" + cli::GenerateDateRegex("%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?"));
  std::cout << date_blocks.size() << "<<\n";
  if (date_blocks.size() == 1) {
    time_t current = time(NULL);
    entry = *localtime(&current);
    LoadTm(date_blocks[0], &entry);
  } else if (date_blocks.size() == 2) {
    time_t current = time(NULL);
    complete = *localtime(&current);
    LoadTm(date_blocks[0], &complete);
    entry = *localtime(&current);
    LoadTm(date_blocks[1], &entry);
  }
  date_blocks.clear();
  date_blocks = cli::RegexFind(
      str, "(due:)" + cli::GenerateDateRegex("%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?"));
  if (date_blocks.size() == 1) {
    time_t current = time(NULL);
    due = *localtime(&current);
    LoadTm(date_blocks[0], &due);
  }

  tags = cli::RegexFind(str, "@[^\\s]+");

  projects = cli::RegexFind(str, "\\+[^\\s]+");

  std::vector<std::string> results = cli::RegexFind(str, "\\(\\d\\)");
  if (results.size() < 1) {
    priority = 0;
  } else {
    priority = int(results[0][1]) - 48;
  }
}

std::string laboris::Task::Print(std::string fmt) {
  std::string str;
  for (int i = 0; i < fmt.size(); i++) {
    if (fmt[i] == '%' && i != fmt.size() - 1) {
      i++;
      if (fmt[i] == 's') {
      } else if (fmt[i] == 'P') {
        str += std::to_string(priority);
      } else if (fmt[i] == 'd') {
        str += description;
      } else if (fmt[i] == 'D') {
        std::string date_fmt = "%Y-%m-%d %H:%M:%S";
        if (i != fmt.size() - 1 && fmt[i + 1] == '{') {
          date_fmt = "";
          i += 2;
          while (i < fmt.size() && fmt[i] != '}') {
            date_fmt += fmt[i];
            i++;
          }
          i++;
        }
        char buffer[255];
        strftime(buffer, 255, date_fmt.c_str(), &due);
        str += std::string(buffer);
      } else if (fmt[i] == 'C') {
        std::string date_fmt = "%Y-%m-%d %H:%M:%S";
        if (i != fmt.size() - 1 && fmt[i + 1] == '{') {
          date_fmt = "";
          i += 2;
          while (i < fmt.size() && fmt[i] != '}') {
            date_fmt += fmt[i];
            i++;
          }
          i++;
        }
        char buffer[255];
        strftime(buffer, 255, date_fmt.c_str(), &complete);
        str += std::string(buffer);
      } else if (fmt[i] == 'E') {
        std::string date_fmt = "%Y-%m-%d %H:%M:%S";
        if (i != fmt.size() - 1 && fmt[i + 1] == '{') {
          date_fmt = "";
          i += 2;
          while (i < fmt.size() && fmt[i] != '}') {
            date_fmt += fmt[i];
            i++;
          }
          i++;
        }
        char buffer[255];
        strftime(buffer, 255, date_fmt.c_str(), &entry);
        str += std::string(buffer);
      } else if (fmt[i] == 't' && i != fmt.size() - 1) {
        i++;
        if (fmt[i] == '*') {
          for (int j = 0; j < tags.size(); j++) {
            str += tags[j];
            if (j != tags.size() - 1) {
              str += " ";
            }
          }
        } else if (fmt[i] >= '0' && fmt[i] <= '9' &&
                   (int)fmt[i] - 48 < tags.size()) {
          str += tags[(int)fmt[i] - 48];
        }
      } else if (fmt[i] == 'p' && i != fmt.size() - 1) {
        i++;
        if (fmt[i] == '*') {
          for (int j = 0; j < projects.size(); j++) {
            str += projects[j];
            if (j != projects.size() - 1) {
              str += " ";
            }
          }
        } else if (fmt[i] >= '0' && fmt[i] <= '9' &&
                   (int)fmt[i] - 48 < projects.size()) {
          str += projects[(int)fmt[i] - 48];
        }
      }
    } else {
      str += fmt[i];
    }
  }
  return str;
}
