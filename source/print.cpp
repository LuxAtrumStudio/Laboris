#include "print.hpp"

#include <stdio.h>
#include <iostream>
#include <vector>

#include "laboris.hpp"
#include "output.hpp"
#include "task.hpp"

void laboris::PrintTasks(unsigned int s, unsigned int sort_method) {
  std::vector<int> sizes = {0, 0, 0, 0, 0, 0, 0};
  std::vector<std::string> fmt = {"%i", "%EC", "%P", "%p*", "%DC", "%d", "%u"};
  std::vector<Task> task_set;
  if (s == 0 || s == 2) {
    SortTasks(sort_method, false, 0);
    task_set.insert(task_set.end(), global_tasks_.begin(), global_tasks_.end());
  }
  if (s == 1 || s == 2) {
    SortTasks(sort_method, false, 1);
    task_set.insert(task_set.end(), completed_tasks_.begin(),
                    completed_tasks_.end());
  }
  if (s == 3) {
    task_set = tmp_task_list_;
  }
  for (int j = 0; j < fmt.size(); j++) {
    for (int i = 0; i < task_set.size(); i++) {
      std::string str = task_set[i].Print(fmt[j]);
      if (str.size() > sizes[j]) {
        sizes[j] = str.size();
      }
    }
  }
  sizes[0] = std::max(sizes[0], 2);
  sizes[1] = std::max(sizes[1], 3);
  sizes[2] = std::max(sizes[2], 1);
  sizes[3] = std::max(sizes[3], 7);
  sizes[4] = std::max(sizes[4], 3);
  sizes[5] = std::max(sizes[5], 11);
  sizes[6] = std::max(sizes[6], 3);
  printf(cli::Underline("%*s %*s %-*s %-*s %-*s %-*s %-5s").c_str(), sizes[0],
         "ID", sizes[1], "Age", sizes[2], "P", sizes[3], "Project", sizes[4],
         "Due", sizes[5], "Description", "Urg");
  std::cout << std::endl;
  for (int i = 0; i < task_set.size(); i++) {
    std::string format = "%*s %*s %-*s %-*s %-*s %-*s %5.2f";
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
    printf(format.c_str(), sizes[0], task_set[i].Print("%i").c_str(), sizes[1],
           task_set[i].Print("%EC").c_str(), sizes[2],
           task_set[i].Print("%P").c_str(), sizes[3],
           task_set[i].Print("%p*").c_str(), sizes[4],
           task_set[i].Print("%DC").c_str(), sizes[5],
           task_set[i].Print("%d").c_str(), task_set[i].urgency);
    printf("\n");
  }
  if (s == 0 || s == 2) {
    SortTasks(SORT_ENTERED, false, 0);
  }
  if (s == 1 || s == 2) {
    SortTasks(SORT_ENTERED, false, 1);
  }
}

void laboris::PrintDetails(Task* task) {
  int size[2] = {4, 5};
  std::vector<std::array<std::string, 2>> opts = {
      {"ID/UUID", "%iu"},   {"Status", "%sl"}, {"Description", "%d"},
      {"Projects", "%p*"},  {"Tags", "%t*"},   {"Entered", "%ED"},
      {"Completed", "%CD"}, {"Due", "%DD"},    {"Priority", "%P"},
      {"Urgency", "%u"}};
  for (int i = 0; i < opts.size(); i++) {
    if (opts[i][0].size() > size[0]) {
      size[0] = opts[i][0].size();
    }
    if (task->Print(opts[i][1]).size() > size[1]) {
      size[1] = task->Print(opts[i][1]).size();
    } else if (task->Print(opts[i][1]).size() == 0) {
      opts.erase(opts.begin() + i);
      i--;
    }
  }
  printf(cli::Underline("%-*s   %-*s  \n").c_str(), size[0], "Name", size[1],
         "Value");
  for (int i = 0; i < opts.size(); i++) {
    std::string str = "%-*s   ";
    if (opts[i][0] == "Projects") {
      str += cli::Blue("%-*s");
    } else if (opts[i][0] == "Tags") {
      str += cli::Magenta("%-*s");
    } else if (opts[i][0] == "Due" && task->OverDue() == true) {
      str += cli::RedBg(cli::White("%-*s"));
    } else if (opts[i][0] == "Due" && task->DueToday() == true) {
      str += cli::YellowBg(cli::Red("%-*s"));
    } else {
      str += "%-*s";
    }
    str += "  ";
    str += "\n";
    if (i % 2 == 0) {
      str = cli::BlackBg(str);
    }
    printf(str.c_str(), size[0], opts[i][0].c_str(), size[1],
           task->Print(opts[i][1]).c_str());
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
