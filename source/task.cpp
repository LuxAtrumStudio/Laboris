#include "task.hpp"

#include <math.h>
#include <time.h>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

#include "regex.hpp"

namespace laboris {
  bool IsInt(std::string str) {
    for (size_t i = 0; i < str.size(); i++) {
      if (str[i] > 57 || str[i] < 48) {
        return false;
      }
    }
    return true;
  }
  bool IsInt(char ch) {
    if (ch > 57 || ch < 48) {
      return false;
    }
    return true;
  }

  bool MatchFmt(std::string str, std::string fmt) {
    if (str.size() > fmt.size()) {
      return false;
    }
    for (size_t i = 0, j = 0; i < fmt.size() && j < str.size(); i++) {
      if (fmt[i] == '%') {
        i++;
        if (fmt[i] == 'i' && (str[j] > 57 || str[j] < 48)) {
          return false;
        }
      } else if (str[j] != fmt[i]) {
        return false;
      }
      j++;
    }
    return true;
  }

  void LoadTm(std::string date, struct tm* t) {
    t->tm_hour = 0;
    t->tm_min = 0;
    t->tm_sec = 0;
    int len = date.size();
    std::string fmt = "-%m-%d";
    if (len == 8 || len == 14 || len == 17) {
      fmt = "%y" + fmt;
    } else if (len == 10 || len == 16 || len == 19) {
      fmt = "%Y" + fmt;
    } else {
      return;
    }
    if (len >= 14) {
      fmt += "T%H:%M";
    }
    if (len >= 17) {
      fmt += ":%S";
    }
    strptime(date.c_str(), fmt.c_str(), t);
  }
}  // namespace laboris

laboris::Task::Task(std::string str) {
  time_t current = time(NULL);
  entry = *localtime(&current);
  complete = *localtime(&current);
  std::vector<std::string> words;
  std::string word;
  std::stringstream ss(str);
  due_ = false;
  while (getline(ss, word, ' ')) {
    words.push_back(word);
  }

  if (words.size() == 0) {
    return;
  }
  if (words[0] == "x" || words[0] == "X") {
    status = DONE;
  } else {
    status = PENDING;
  }
  unsigned int current_date = 0;
  for (size_t i = 0; i < words.size(); i++) {
    bool done = false;
    if (i == 0 && (words[i] == "x" || words[i] == "X")) {
      done = true;
    }
    if (done == false && words[i][0] == '+') {
      words[i].erase(words[i].begin());
      projects.push_back(words[i]);
      done = true;
    }
    if (done == false && words[i][0] == '@') {
      words[i].erase(words[i].begin());
      tags.push_back(words[i]);
      done = true;
    }
    if (done == false && words[i][0] == '(' && words[i].back() == ')') {
      std::string pri = words[i];
      pri.erase(pri.begin());
      pri.pop_back();
      if (IsInt(pri) == true) {
        priority = stoi(pri);
        done = true;
      }
    }
    if (done == false && words[i].size() > 4 && words[i][0] == 'd' &&
        words[i][1] == 'u' && words[i][2] == 'e' && words[i][3] == ':') {
      words[i].erase(words[i].begin(), words[i].begin() + 4);
      due = *localtime(&current);
      LoadTm(words[i], &due);
      due_ = true;
      done = true;
    }
    if (done == false &&
        (MatchFmt(words[i], "%i%i%i%i-%i%i-%i%iT%i%i:%i%i:%i%i") ||
         MatchFmt(words[i], "%i%i-%i%i-%i%iT%i%i:%i%i:%i%i") ||
         MatchFmt(words[i], "%i%i%i%i-%i%i-%i%iT%i%i:%i%i") ||
         MatchFmt(words[i], "%i%i-%i%i-%i%iT%i%i:%i%i") ||
         MatchFmt(words[i], "%i%i%i%i-%i%i-%i%i") ||
         MatchFmt(words[i], "%i%i-%i%i-%i%i")) == true) {
      if (current_date == 0) {
        LoadTm(words[i], &entry);
        done = true;
        current_date = 1;
      } else if (current_date == 1) {
        complete = entry;
        LoadTm(words[i], &entry);
        done = true;
        current_date = 2;
      }
    } else if (done == false) {
      description += words[i] + " ";
    }
  }
  description.pop_back();

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

bool laboris::Task::DueToday() {
  if (due_ == false) {
    return false;
  }
  time_t current_time = time(NULL);
  struct tm current = *localtime(&current_time);
  if (current.tm_year == due.tm_year && current.tm_mon == due.tm_mon &&
      current.tm_mday == due.tm_mday && status != DONE) {
    return true;
  } else {
    return false;
  }
}

bool laboris::Task::OverDue() {
  if (due_ == false) {
    return false;
  }
  time_t current_time = time(NULL);
  struct tm current = *localtime(&current_time);
  if (current.tm_year >= due.tm_year && current.tm_mon >= due.tm_mon &&
      current.tm_mday >= due.tm_mday && current.tm_hour >= due.tm_hour &&
      current.tm_min >= due.tm_min && current.tm_sec > due.tm_sec &&
      status != DONE) {
    return true;
  }
  return false;
}

void laboris::Task::GenerateUuid() {
  time_t entry_time = mktime(&entry);
  uuid = entry_time;
  for (int i = 0; i < description.size(); i++) {
    uuid += int(description[i]);
  }
}

void laboris::Task::LoadUrgency() {
  urgency = 0;
  urgency += fabs(2.000 * UrgencyAge());
  urgency += fabs(12.00 * UrgencyDue());
  urgency += fabs(0.200 * UrgencyTags());
  urgency += fabs(1.000 * UrgencyPriority());
  urgency += fabs(1.000 * UrgencyProjects());
  if (status == DONE) {
    urgency = 0;
  }
}

std::string laboris::Task::GetDateString(std::string str, int& i) {
  std::string date_fmt = "%Y-%m-%d %H:%M:%S";
  std::string date_str = "";
  int i_0 = i;
  if (i != str.size()) {
    if (str[i + 1] == 'C') {
      date_fmt = "";
      std::array<int, 6> steps = {60, 60, 24, 7, 4, 12};
      std::array<char, 6> step_suffix = {'m', 'h', 'd', 'W', 'M', 'Y'};
      time_t date_time;
      if (str[i_0] == 'D') {
        date_time = mktime(&due);
      } else if (str[i_0] == 'E') {
        date_time = mktime(&entry);
      } else if (str[i_0] == 'C') {
        date_time = mktime(&entry);
      }
      time_t current = time(NULL);
      date_time -= current;
      if (date_time < 0) {
        if (str[i_0] != 'E') {
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
  if (str[i_0] == 'D') {
    strftime(buffer, 255, date_fmt.c_str(), &due);
  } else if (str[i_0] == 'C') {
    strftime(buffer, 255, date_fmt.c_str(), &complete);
  } else if (str[i_0] == 'E') {
    strftime(buffer, 255, date_fmt.c_str(), &entry);
  }
  date_str += std::string(buffer);
  if (due_ == false) {
    return "";
  }
  return date_str;
}

double laboris::Task::UrgencyAge() {
  time_t now = time(NULL);
  time_t e = mktime(&entry);
  double age = (now - e) / 86400.0;
  return (1.0 * age / 400.0);
}

double laboris::Task::UrgencyDue() {
  if (due_ == true) {
    time_t now = time(NULL);
    time_t d = mktime(&due);
    double overdue = (double)(now - d) / 86400.0;
    if (overdue >= 7.0) {
      return 1.0;
    } else if (overdue >= -14.0) {
      return ((overdue + 14.0) * 0.8 / 21.0) + 0.2;
    } else {
      return 0.2;
    }
  }
  return 0.0;
}

double laboris::Task::UrgencyTags() { return tags.size(); }

double laboris::Task::UrgencyPriority() {
  if (priority == 0) {
    return 0.0;
  }
  return 6.0 / (double)priority;
}

double laboris::Task::UrgencyProjects() { return projects.size(); }
