#include "print.hpp"

#include <stdio.h>
#include <iostream>
#include <vector>

#include "laboris.hpp"
#include "output.hpp"
#include "task.hpp"

void laboris::PrintTasks(unsigned int s) {
  std::vector<int> sizes = {0, 0, 0, 0, 0, 0};
  std::vector<std::string> fmt = {"%EC", "%P", "%p*", "%DC", "%d", "%u"};
  std::vector<Task> task_set;
  if (s == 0 || s == 2) {
    task_set.insert(task_set.end(), global_tasks_.begin(), global_tasks_.end());
  }
  if (s == 1 || s == 2) {
    task_set.insert(task_set.end(), completed_tasks_.begin(),
                    completed_tasks_.end());
  }
  for (int j = 0; j < fmt.size(); j++) {
    for (int i = 0; i < task_set.size(); i++) {
      std::string str = task_set[i].Print(fmt[j]);
      if (str.size() > sizes[j]) {
        sizes[j] = str.size();
      }
    }
  }
  sizes[0] = std::max(sizes[0], 3);
  sizes[1] = std::max(sizes[1], 1);
  sizes[2] = std::max(sizes[2], 7);
  sizes[3] = std::max(sizes[3], 3);
  sizes[4] = std::max(sizes[4], 11);
  sizes[5] = std::max(sizes[5], 3);
  printf(cli::Underline("%*s %*s %-*s %-*s %-*s %-*s %-5s").c_str(), 2, "ID",
         sizes[0], "Age", sizes[1], "P", sizes[2], "Project", sizes[3], "Due",
         sizes[4], "Description", "Urg");
  std::cout << std::endl;
  for (int i = 0; i < task_set.size(); i++) {
    std::string format = "%*i %*s %-*s %-*s %-*s %-*s %5.2f";
    if (task_set[i].status == DONE) {
      format = cli::LightBlack(format);
    }
    if (task_set[i].DueToday() == true) {
      format = cli::YellowBg(cli::Red(format));
    } else if (task_set[i].OverDue() == true) {
      format = cli::RedBg(cli::White(format));
    }
    if (task_set[i].urgency >= 10) {
      format = cli::Bold(cli::Red(format));
    } else if (task_set[i].urgency >= 9) {
      format = cli::Red(format);
    } else if (task_set[i].urgency >= 8) {
      format = cli::LightYellow(format);
    } else if (task_set[i].urgency >= 7) {
      format = cli::Yellow(format);
    }
    if (i % 2 == 0) {
      format = cli::BlackBg(format);
    }
    printf(format.c_str(), 2, i + 1, sizes[0], task_set[i].Print("%EC").c_str(),
           sizes[1], task_set[i].Print("%P").c_str(), sizes[2],
           task_set[i].Print("%p*").c_str(), sizes[3],
           task_set[i].Print("%DC").c_str(), sizes[4],
           task_set[i].Print("%d").c_str(), task_set[i].urgency);
    printf("\n");
  }
}

void laboris::PrintDetails(int id) {
  int size[2] = {4, 5};
  std::vector<std::array<std::string, 2>> opts = {
      {"Status", "%sl"},  {"Description", "%d"}, {"Projects", "%p*"},
      {"Tags", "%t*"},    {"Entered", "%ED"},    {"Due", "%DD"},
      {"Priority", "%P"}, {"Urgency", "%u"}};
  for (int i = 0; i < opts.size(); i++) {
    if (opts[i][0].size() > size[0]) {
      size[0] = opts[i][0].size();
    }
    if (global_tasks_[id].Print(opts[i][1]).size() > size[1]) {
      size[1] = global_tasks_[id].Print(opts[i][1]).size();
    }
  }
  printf(cli::Underline("%-*s   %-*s\n").c_str(), size[0], "Name", size[1],
         "Value");
  printf("%-*s   %-*i\n", size[0], "ID", size[1], id + 1);
  for (int i = 0; i < opts.size(); i++) {
    std::string str = "%-*s   ";
    if (opts[i][0] == "Projects") {
      str += cli::Blue("%-*s");
    } else if (opts[i][0] == "Tags") {
      str += cli::Magenta("%-*s");
    } else if (opts[i][0] == "Due" && global_tasks_[id].OverDue() == true) {
      str += cli::RedBg(cli::White("%-*s"));
    } else if (opts[i][0] == "Due" && global_tasks_[id].DueToday() == true) {
      str += cli::YellowBg(cli::Red("%-*s"));
    } else {
      str += "%-*s";
    }
    str += "\n";
    if (i % 2 == 0) {
      str = cli::BlackBg(str);
    }
    printf(str.c_str(), size[0], opts[i][0].c_str(), size[1],
           global_tasks_[id].Print(opts[i][1]).c_str());
  }
}

void laboris::PrintAction(std::vector<std::string> data,
                          std::vector<int> colors) {
  for (int i = 0, j = 0; i < data.size(); i++, j++) {
    std::string fmt = "%s\n";
    if (j == colors.size()) {
      j = 0;
    }
    fmt = cli::ColorFg(fmt, colors[j]);
    printf(fmt.c_str(), data[i].c_str());
  }
}
