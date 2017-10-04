#include <pwd.h>
#include <sys/types.h>
#include <unistd.h>
#include <iostream>
#include <vector>

#include "laboris.hpp"

int main(int argc, char const* argv[]) {
  std::string file_path = "";
  struct passwd* pw = getpwuid(getuid());
  const char* homedir = pw->pw_dir;
  file_path = std::string(homedir) + "/.laboris/todo.txt";
  if (argc > 1) {
    if (laboris::IsFile(argv[1]) == true) {
      file_path = std::string(argv[1]);
      for (int i = 1; i < argc; ++i) {
        argv[i] = argv[i + 1];  // copy next element left
      }
      argc--;
    }
  }
  laboris::LoadTasks(file_path);
  laboris::ParseOptions(argc, argv);
  laboris::SaveTasks(file_path);
  return 0;
}
