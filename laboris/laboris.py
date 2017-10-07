import load_data as load_data
import task
from datetime import datetime


def main():
    my_task = task.Task("This is a test task", ["project 1", "project 2", "project 3", "project 4"],
                        ["tag 1", "tag 2", "tag 3", "tag 4", "tag 5"], 5, datetime.now(), datetime(2017, 10, 7, 16))
    print(my_task.print_date_due())
    print(my_task.print_date_entry("abbr"))
    print(my_task.print_date_due("abbr"))


if __name__ == "__main__":
    main()
