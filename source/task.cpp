#include "task.hpp"

#include <math.h>
#include <time.h>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

#include "regex.hpp"

namespace laboris {
  void LoadTm(std::string date, struct tm* t) {
    t->tm_hour = 0;
    t->tm_min = 0;
    t->tm_sec = 0;
    if (cli::Regex(date, cli::GenerateDateRegex("%Y-%m-%dT%H:%M:%S")) == true) {
      strptime(date.c_str(), "%Y-%m-%dT%H:%M:%S", t);
    } else if (cli::Regex(date, cli::GenerateDateRegex("%Y-%m-%dT%H:%M")) ==
               true) {
      strptime(date.c_str(), "%Y-%m-%dT%H:%M", t);
    } else if (cli::Regex(date, cli::GenerateDateRegex("%Y-%m-%d")) == true) {
      strptime(date.c_str(), "%Y-%m-%d", t);
    }
  }
}  // namespace laboris

laboris::Task::Task(std::string str) {
  if (str.size() == 0) {
    return;
  }
  if (str[0] == 'x' || str[0] == 'X') {
    status = DONE;
  } else {
    status = PENDING;
  }
  std::vector<std::string> date_blocks = cli::RegexFind(
      str, "\\s" + cli::GenerateDateRegex("%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?"));
  if (date_blocks.size() == 1) {
    time_t current = time(NULL);
    entry = *localtime(&current);
    date_blocks[0].erase(date_blocks[0].begin());
    LoadTm(date_blocks[0], &entry);
  } else if (date_blocks.size() == 2) {
    time_t current = time(NULL);
    complete = *localtime(&current);
    date_blocks[0].erase(date_blocks[0].begin());
    LoadTm(date_blocks[0], &complete);
    entry = *localtime(&current);
    date_blocks[1].erase(date_blocks[1].begin());
    LoadTm(date_blocks[1], &entry);
  }
  date_blocks.clear();
  date_blocks = cli::RegexFind(
      str, "(due:)" + cli::GenerateDateRegex("%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?"));
  if (date_blocks.size() == 1) {
    time_t current = time(NULL);
    due = *localtime(&current);
    date_blocks[0].erase(date_blocks[0].begin(), date_blocks[0].begin() + 4);
    LoadTm(date_blocks[0], &due);
    due_ = true;
  } else {
    due_ = false;
  }

  tags = cli::RegexFind(str, "@[^\\s]+");

  projects = cli::RegexFind(str, "\\+[^\\s]+");

  std::vector<std::string> results = cli::RegexFind(str, "\\(\\d\\)");
  if (results.size() < 1) {
    priority = 0;
  } else {
    priority = int(results[0][1]) - 48;
  }

  std::stringstream ss(str);
  std::string line;
  while (std::getline(ss, line, ' ')) {
    if (line != "x" && line != "X" && cli::Regex(line, "\\(\\d\\)") == false &&
        cli::Regex(line, "\\+.+") == false &&
        cli::Regex(line, "@.+") == false &&
        cli::Regex(line,
                   "(due:)" + cli::GenerateDateRegex(
                                  "%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?")) == false &&
        cli::Regex(line, cli::GenerateDateRegex(
                             "%Y-%m-%d%(T%H:%M%(:%S%)%?%)%?")) == false) {
      description += line + " ";
    }
  }
  GenerateUuid();
  LoadUrgency();
}

std::string laboris::Task::Print(std::string fmt) {
  std::string str;
  for (int i = 0; i < fmt.size(); i++) {
    if (fmt[i] == '%' && i != fmt.size() - 1) {
      i++;
      if (fmt[i] == 's') {
        if (status == DONE) {
          str += "C";
        } else if (status == PENDING) {
          str += "P";
        }
      } else if (fmt[i] == 'S') {
        if (status == DONE) {
          str += "X";
        } else if (status == PENDING) {
          str += " ";
        }
      } else if (fmt[i] == 'P') {
        str += std::to_string(priority);
      } else if (fmt[i] == 'd') {
        str += description;
      } else if (fmt[i] == 'u') {
        std::stringstream ss;
        ss << std::fixed << std::setprecision(2) << urgency;
        str += ss.str();
      } else if (fmt[i] == 'D') {
        str += GetDateString(fmt, i);
      } else if (fmt[i] == 'C') {
        str += GetDateString(fmt, i);
      } else if (fmt[i] == 'E') {
        str += GetDateString(fmt, i);
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

void laboris::Task::GenerateUuid() {
  time_t entry_time = mktime(&entry);
  uuid = entry_time;
  for (int i = 0; i < description.size(); i++) {
    uuid += int(description[i]);
  }
}

void laboris::Task::LoadUrgency() {
  time_t current = time(NULL);
  urgency = 0;
  if (priority != 0) {
    urgency += (6 / priority);
  }
  urgency += (tags.size() * 0.5);
  urgency += (projects.size() * 1.0);
  time_t entry_time = mktime(&entry);
  entry_time = current - entry_time;
  double age_val = 0.00362 * pow(2, -(double(entry_time) / 604800.0));
  urgency += (age_val * 2.0);
  if (due_ == true) {
    time_t due_time = mktime(&due);
    due_time = due_time - current;
    double due_val = 0.75 / pow(2, double(due_time) / 604800.0);
    urgency += (due_val * 12.0);
  }
  if (status == DONE) {
    urgency = 0;
  }
}

std::string laboris::Task::GetDateString(std::string str, int& i) {
  std::string date_fmt = "%Y-%m-%d %H:%M:%S";
  std::string date_str = "";
  if (i != str.size()) {
    if (str[i + 1] == 'C') {
      date_fmt = "";
      std::array<int, 6> steps = {60, 60, 24, 7, 4, 12};
      std::array<char, 6> step_suffix = {'m', 'h', 'd', 'W', 'M', 'Y'};
      time_t date_time;
      if (str[i] == 'D') {
        date_time = mktime(&due);
      } else if (str[i] == 'E') {
        date_time = mktime(&entry);
      } else if (str[i] == 'C') {
        date_time = mktime(&entry);
      }
      time_t current = time(NULL);
      date_time -= current;
      if (date_time < 0) {
        if (str[i] != 'E') {
          date_str += '-';
        }
        date_time *= -1;
      }
      if (date_time == 0) {
        date_str += "NOW";
      } else {
        char suffix = 's';
        for (int j = 0; j < 6; j++) {
          if (date_time > steps[j]) {
            date_time /= steps[j];
            suffix = step_suffix[j];
          } else {
            break;
          }
        }
        date_str += std::to_string(date_time) + suffix;
      }
      i++;
    } else if (str[i + 1] == '{') {
      date_fmt = "";
      i += 2;
      while (i < str.size() && str[i] != '}') {
        date_fmt += str[i];
        i++;
      }
    }
  }
  char buffer[255];
  strftime(buffer, 255, date_fmt.c_str(), &entry);
  date_str += std::string(buffer);
  if (due_ == false) {
    return "";
  }
  return date_str;
}
