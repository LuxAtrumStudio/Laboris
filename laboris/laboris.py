#!/usr/bin/python3

import data
import parser


def main():
    pending, done = data.load_data()
    parser.parse_args(pending, done)
    data.save_data(pending, done)


if __name__ == "__main__":
    main()
