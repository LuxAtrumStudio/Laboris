from color import fg, bg, stylize, attr

def print_entry(task, fmt, spacing=2):
    fmt = fmt.split('|')
    output = str()
    for part in fmt:
        if part == "id":
            output += "{}".format(task.id + 1)
        elif part.startswith("entry"):
            tmp = part.split(';')
            if len(tmp) >= 2:
                output += task.print_date_entry(tmp[1])
            else:
                output += task.print_date_entry("abbr")
        elif part == "project":
            output += task.print_project()
        elif part == "due":
            tmp = part.split(';')
            if len(tmp) >= 2:
                output += task.print_date_due(tmp[1])
            else:
                output += task.print_date_due("abbr")
        elif part == "description":
            output += task.description
        elif part == "urgency":
            output += "{:.4}".format(task.urgency)
        output += ' ' * spacing
    if task.is_overdue() is True:
        output = stylize(output, [fg('white'), bg('red')])
    elif task.due_today() is True:
        output = stylize(output, [fg('red'), bg('yellow')])
    elif task.urgency > 10:
        output = stylize(output, [fg('red'), attr('bold')])
    elif task.urgency > 8.5:
        output = stylize(output, [fg('red')])
    elif task.urgency > 7:
        output = stylize(output, [fg('yellow')])
    return output


def print_set(tasks, fmt=None):
    if fmt is None:
        fmt = "id|entry|project|due|description|urgency"
    for i, t in enumerate(tasks):
        if i % 2 != 0:
            print("{}{}{}".format(bg('black'), print_entry(t, fmt), attr('reset')))
        else:
            print("{}".format(print_entry(t, fmt)))
            # print("{}".format(t))
