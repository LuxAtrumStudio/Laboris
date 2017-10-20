#!/usr/bin/python3

import settings as s
import printer
import sorter
import parser
import os


def main():
    s.init()
    s._theme.parse_file(os.path.expanduser("~/.laboris/default.json"))
    # s._theme.set_color("report.burndown.active")
    # print("YES")
    parser.parse_args()
    s.term()
    # sorter.sort_task_set(s._pending, "urg")
    # printer.print_task_set(s._pending)
    # printer.print_task_details(s._pending[2])
    # print(s._pending[0].task_color(s._pending[0].print_fmt(
    #     "id|description|due|age;abbr|urg")))


if __name__ == "__main__":
    main()
