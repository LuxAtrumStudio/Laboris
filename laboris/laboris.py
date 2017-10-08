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
        # print(out.red("{}").format(t.get_json()))
        print(stylize("Hello World", [fg('light_red'), attr('underlined')]))
        print("{}{}{}".format(bg('light_red'), "Hello", attr('reset')))


if __name__ == "__main__":
    main()
