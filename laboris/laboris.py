#!/usr/bin/python3

import data
import task
from color import fg, bg, attr, stylize
import print
from datetime import datetime


def main():
    pending, done = data.load_data()
    print.print_set(pending)
    data.save_data(pending, done)


if __name__ == "__main__":
    main()
