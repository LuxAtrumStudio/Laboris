#!/usr/bin/python3

import laboris.settings as s
import laboris.parser as parser
import os


def main():
    s.init()
    s._theme.parse_file(os.path.expanduser("~/.laboris/default.json"))
    parser.parse_args()
    s.term()


if __name__ == "__main__":
    main()
