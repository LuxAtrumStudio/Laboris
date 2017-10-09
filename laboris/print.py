from color import fg, bg, stylize, attr


def print_entry(task, fmt, sizes, spacing=2):
    fmt = fmt.split('|')
    output = str()
    for i, part in enumerate(fmt):
        if part == "description":
            output += "{:{}}".format(task.description, sizes[i])
        elif part == "project":
            output += "{:{}}".format(task.print_project(), sizes[i])
        elif part == "tag":
            output += task.print_tag()
        elif part == "uuid":
            output += task.uuid
        elif part == "priority":
            output += str(task.priority)
        elif part == "urgency":
            output += "{:.4}".format(task.urgency)
        elif part.startswith("entry"):
            tmp = part.split(';')
            if len(tmp) >= 2:
                output += task.print_date_entry(tmp[1])
            else:
                output += task.print_date_entry()
        elif part == "due":
            tmp = part.split(';')
            if len(tmp) >= 2:
                output += task.print_date_due(tmp[1])
            else:
                output += task.print_date_due()
        elif part == "done":
            tmp = part.split(';')
            if len(tmp) >= 2:
                output += task.print_date_done(tmp[1])
            else:
                output += task.print_date_done()
        elif part == "status":
            tmp = part.split(';')
            if len(tmp) > 1:
                output += task.print_status(tmp[1])
            else:
                output += task.print_status()
        elif part == "id":
            output += str(task.id)
        elif part == "times":
            tmp = part.split(';')
            if len(tmp) > 1:
                output += task.print_interval(tmp[1])
            else:
                output += task.print_interval()
        output += ' ' * spacing
    output = output[:-2]
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


def print_line(line, index):
    if index % 2 != 0:
        print("{}{}{}".format(bg('black'), line, attr('reset')))
    else:
        print("{}".format(line))


def get_max_size(tasks, term):
    m = len(term)
    for t in tasks:
        if term == "description":
            m = max(m, len(t.description))
        elif term == "project":
            m = max(m, len(t.print_project()))
        elif term == "tag":
            m = max(m, len(t.print_tag()))
        elif term == "uuid":
            m = max(m, len(t.uuid))
        elif term == "priority":
            m = max(m, len(t.priority))
        elif term == "urgency":
            m = max(m, len("{:.4}".format(t.urgency)))
        elif term.startswith("entry"):
            tmp = term.split(';')
            if len(tmp) > 1:
                m = max(m, len(t.print_date_entry(tmp[1])))
            else:
                m = max(m, len(t.print_date_entry()))
        elif term.startswith("due"):
            tmp = term.split(';')
            if len(tmp) > 1:
                m = max(m, len(t.print_date_due(tmp[1])))
            else:
                m = max(m, len(t.print_date_due()))
        elif term.startswith("done"):
            tmp = term.split(';')
            if len(tmp) > 1:
                m = max(m, len(t.print_date_done(tmp[1])))
            else:
                m = max(m, len(t.print_date_done()))
        elif term == "id":
            m = max(m, len(str(t.id)))
        elif term.startswith("status"):
            tmp = term.split(';')
            if len(tmp) > 1:
                m = max(m, len(t.print_status(tmp[1])))
            else:
                m = max(m, len(t.print_status()))
        elif term.startswith("times") and len(t.times) != 0:
            tmp = term.split(';')
            if len(tmp) > 1:
                m = max(m, len(t.print_interval(tmp[1], False, 0)))
            else:
                m = max(m, len(t.print_interval(None, False, 0)))

    return m


def print_set(tasks, fmt=None):
    if fmt is None:
        fmt = "id|entry|project|due|description|urgency"
    parts = fmt.split('|')
    sizes = []
    for p in parts:
        sizes.append(get_max_size(tasks, p))
    for i, p in enumerate(parts):
        p = p.split(';')[0]
        print(stylize("{:{}}", [fg('white'), attr('underlined')]).format(p.title(), sizes[i]), end='  ')
    print()
    for i, t in enumerate(tasks):
        print_line(print_entry(t, fmt, sizes), i)


def print_task(task, fmt=None):
    if fmt is None:
        fmt = "id|description|status;long|project|tag|entry|due|done|urgency|times"
    fmt = fmt.split('|')
    name_size = 4
    for part in fmt:
        part = part.split(';')
        name_size = max(name_size, len(part[0]))
    value_size = 5
    for part in fmt:
        if part == "description":
            value_size = max(value_size, len(task.description))
        elif part == "project" and len(task.project) != 0:
            value_size = max(value_size, len(max(task.project, key=len)))
        elif part == "tag" and len(task.tag) != 0:
            value_size = max(value_size, len(max(task.tag, key=len)))
        elif part == "uuid":
            value_size = max(value_size, len(task.uuid))
        elif part == "priority":
            value_size = max(value_size, len(task.priority))
        elif part == "urgency":
            value_size = max(value_size, len("{:.04}".format(task.urgency)))
        elif part.startswith("entry"):
            tmp = part.split(';')
            if len(tmp) > 1:
                value_size = max(value_size, len(task.print_date_entry(tmp[1])))
            else:
                value_size = max(value_size, len(task.print_date_entry()))
        elif part.startswith("due"):
            tmp = part.split(';')
            if len(tmp) > 1:
                value_size = max(value_size, len(task.print_date_due(tmp[1])))
            else:
                value_size = max(value_size, len(task.print_date_due()))
        elif part.startswith("done"):
            tmp = part.split(';')
            if len(tmp) > 1:
                value_size = max(value_size, len(task.print_date_done(tmp[1])))
            else:
                value_size = max(value_size, len(task.print_date_done()))
        elif part == "id":
            value_size = max(value_size, len(str(task.id)))
        elif part.startswith("status"):
            tmp = part.split(';')
            if len(tmp) > 1:
                value_size = max(value_size, len(task.print_status(tmp[1])))
            else:
                value_size = max(value_size, len(task.print_status()))
        elif part.startswith("times") and len(task.times) != 0:
            tmp = part.split(';')
            if len(tmp) > 1:
                value_size = max(value_size, len(task.print_interval(tmp[1], False, 0)))
            else:
                value_size = max(value_size, len(task.print_interval(None, False, 0)))

    print(stylize("{:{}}", [attr('underlined'), fg('white')]).format("Name", name_size), end='   ')
    print(stylize("{:{}}", [attr('underlined'), fg('white')]).format("Value", value_size))
    index = 0
    for part in fmt:
        if part == "description":
            index += 1
            print_line("{:{}}   {:{}}".format("Description", name_size, task.description, value_size), index)
        elif part == "project" and len(task.project) != 0:
            index += 1
            for j, p in enumerate(task.project):
                if j == 0:
                    print_line("{:{}}   {:{}}".format("Projects", name_size, task.print_project(j), value_size), index)
                else:
                    print_line("{:{}}   {:{}}".format("", name_size, task.print_project(j), value_size), index)
                index += 1
            index -= 1
        elif part == "tag" and len(task.tag) != 0:
            index += 1
            for j, p in enumerate(task.tag):
                if j == 0:
                    print_line("{:{}}   {:{}}".format("Tags", name_size, task.print_tag(j), value_size), index)
                else:
                    print_line("{:{}}   {:{}}".format("", name_size, task.print_tag(j), value_size), index)
                index += 1
            index -= 1
        elif part == "uuid":
            index += 1
            print_line("{:{}}   {:{}}".format("UUID", name_size, task.uuid, value_size), index)
        elif part == "priority":
            index += 1
            print_line("{:{}}   {:{}}".format("Priority", name_size, str(task.priority), value_size), index)
        elif part == "urgency":
            index += 1
            print_line("{:{}}   {:{}}".format("Urgency", name_size, "{:.04}".format(task.urgency), value_size), index)
        elif part.startswith("entry") and task.entry_date is not None:
            index += 1
            tmp = part.split(';')
            if len(tmp) > 1:
                print_line("{:{}}   {:{}}".format("Entry", name_size, task.print_date_entry(tmp[1]), value_size), index)
            else:
                print_line("{:{}}   {:{}}".format("Entry", name_size, task.print_date_entry(), value_size), index)
        elif part.startswith("due") and task.due_date is not None:
            index += 1
            tmp = part.split(';')
            if len(tmp) > 1:
                print_line("{:{}}   {:{}}".format("Due", name_size, task.print_date_due(tmp[1]), value_size), index)
                value_size = max(value_size, len(task.print_date_due(tmp[1])))
            else:
                print_line("{:{}}   {:{}}".format("Due", name_size, task.print_date_due(), value_size), index)
        elif part.startswith("done") and task.done_date is not None:
            index += 1
            tmp = part.split(';')
            if len(tmp) > 1:
                print_line("{:{}}   {:{}}".format("Done", name_size, task.print_date_done(tmp[1]), value_size), index)
            else:
                print_line("{:{}}   {:{}}".format("Done", name_size, task.print_date_done(), value_size), index)
        elif part == "id":
            index += 1
            print_line("{:{}}   {:{}}".format("ID", name_size, str(task.id), value_size), index)
        elif part.startswith("status"):
            index += 1
            tmp = part.split(';')
            if len(tmp) > 1:
                print_line("{:{}}   {:{}}".format("Status", name_size, task.print_status(tmp[1]), value_size), index)
            else:
                print_line("{:{}}   {:{}}".format("Status", name_size, task.print_status(), value_size), index)
        elif part.startswith("times") and len(task.times) != 0:
            index += 1
            tmp = part.split(';')
            if len(tmp) > 1:
                tmp = tmp[1]
            else:
                tmp = None
            for j, t in enumerate(task.times):
                if j == 0:
                    print_line(
                        "{:{}}   {:{}}".format("Times", name_size, task.print_interval(tmp, False, j), value_size),
                        index)
                else:
                    print_line("{:{}}   {:{}}".format("", name_size, task.print_interval(tmp, False, j), value_size),
                               index)
                index += 1
            index -= 1
