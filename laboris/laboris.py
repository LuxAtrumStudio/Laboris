import data
import task
from color import fg, bg, attr, stylize
from datetime import datetime


def main():
    pending, done = data.load_data()
    print("PENDING: {}\nDONE: {}".format(len(pending), len(done)))
    for t in pending:
        print("{} {} {} {}".format(t.print_date_entry("abbr"), t.print_date_due("abbr"), t.print_project(),
                                   t.description))
        print("{} -> {}: {}".format(t.print_interval("start", True), t.print_interval("end", True),
                                    t.print_interval("duration", True)))
    data.save_data(pending, done)


if __name__ == "__main__":
    main()
