#include "print.hpp"

#include <stdio.h>
#include <iostream>
#include <vector>

#include "output.hpp"
#include "task.hpp"

void laboris::PrintTasks(std::vector<Task> tasks) {
  std::vector<int> sizes = {0, 0, 0, 0, 0, 0};
  std::vector<std::string> fmt = {"%EC", "%P", "%p*", "%DC", "%d", "%u"};
  for (int j = 0; j < fmt.size(); j++) {
    for (int i = 0; i < tasks.size(); i++) {
      std::string str = tasks[i].Print(fmt[j]);
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
  printf(cli::Underline("%*s %*s %-*s %-*s %-*s %-*s %-*s").c_str(), 2, "ID",
         sizes[0], "Age", sizes[1], "P", sizes[2], "Project", sizes[3], "Due",
         sizes[4], "Description", sizes[5], "Urg");
  std::cout << std::endl;
  for (int i = 0; i < tasks.size(); i++) {
    std::string format = "%*i %*s %-*s %-*s %-*s %-*s %-*s";
    if (tasks[i].status == DONE) {
      format = cli::LightBlack(format);
    }
    if (tasks[i].urgency >= 10) {
      format = cli::Bold(cli::Red(format));
    } else if (tasks[i].urgency >= 9) {
      format = cli::LightRed(format);
    } else if (tasks[i].urgency >= 8) {
      format = cli::Red(format);
    } else if (tasks[i].urgency >= 7) {
      format = cli::Bold(cli::Yellow(format));
    } else if (tasks[i].urgency >= 6) {
      format = cli::LightYellow(format);
    } else if (tasks[i].urgency >= 5) {
      format = cli::Yellow(format);
    } else if (tasks[i].urgency >= 4) {
      format = cli::Green(format);
    } else if (tasks[i].urgency >= 3) {
      format = cli::LightGreen(format);
    } else if (tasks[i].urgency >= 2) {
      format = cli::Bold(cli::Green(format));
    }
    if (i % 2 == 0) {
      format = cli::BlackBg(format);
    }
    printf(format.c_str(), 2, i + 1, sizes[0], tasks[i].Print("%EC").c_str(),
           sizes[1], tasks[i].Print("%P").c_str(), sizes[2],
           tasks[i].Print("%p*").c_str(), sizes[3],
           tasks[i].Print("%DC").c_str(), sizes[4],
           tasks[i].Print("%d").c_str(), sizes[5],
           tasks[i].Print("%u").c_str());
    printf("\n");
  }
}
