"""
Summary report
"""
import datetime
import math
import laboris.task as ltask
from laboris.color import Attr, WAttr
from laboris.config import CONFIG
from laboris.smart_datetime import new


def gen_progres_bar(width, perc):
    colors = [
        "E50900", "E51200", "E51A00", "E62200", "E62B01", "E73301", "E73B01",
        "E74402", "E84C02", "E85402", "E95C02", "E96503", "E96D03", "EA7603",
        "EA7E04", "EB8604", "EB8F04", "EC9704", "ECA005", "ECA805", "EDB005",
        "EDB906", "EEC106", "EECA06", "EED207", "EFDB07", "EFE307", "F0EC08",
        "ECF008", "E4F008", "DDF109", "D5F109", "CDF209", "C6F209", "BEF30A",
        "B6F30A", "AFF30A", "A7F40B", "9FF40B", "97F50B", "90F50C", "88F50C",
        "80F60C", "78F60D", "71F70D", "69F70D", "61F70E", "59F80E", "52F80E",
        "4AF90F", "42F90F", "3AFA0F", "32FA10", "2BFA10", "23FB10", "1BFB11",
        "13FC11", "11FC17", "12FC20", "12FD28", "12FD31", "13FE39", "13FE42",
        "14FF4B"
    ]
    colors = ["F44336", "FF5722", "FF9800", "FFC107", "FFEB3B", "CDDC39", "8BC34A", "4CAF50"]
    color = colors[math.floor(perc * (len(colors) - 1))]
    return WAttr(" " * int(width * perc), width, color, bg=True)


def summary_report(args):
    cat = 'ndone'
    types = 'both'
    start = None
    end = None
    for arg in args:
        if arg in ['pending', 'all', 'completed', 'ndone']:
            cat = arg
        elif arg in ['both', 'project', 'task']:
            types = arg
        elif start is None:
            start = new(arg).timestamp()
        elif end is None:
            end = new(arg).timestamp()
    if start is None:
        start = 0
    if end is None:
        end = datetime.datetime.now().timestamp()
    projects = {}
    
    print(cat, types)

    def append_proj(proj, contrib):
        if proj in projects:
            projects[proj][0] += contrib[0]
            projects[proj][1] += contrib[1]
            projects[proj][2] += contrib[2]
        else:
            projects[proj] = contrib

    if cat in ('pending', 'all', 'ndone'):
        for uuid, task in ltask.PENDING.items():
            if task['entryDate'] < end and task['modifiedDate'] > start:
                tt = 0
                for time in task['times']:
                    if start < time[0] < end:
                        if len(time) == 2:
                            tt += (time[1] - time[0])
                        else:
                            tt += (
                                datetime.datetime.now().timestamp() - time[0])
                for proj in task['projects']:
                    if types in ('both', 'project'):
                        append_proj(proj, [1, 0, tt])
                if not task['projects'] and types in ('both', 'task'):
                    append_proj(task['title'], [1, 0, tt])
    if cat in ('all', 'completed', 'ndone'):
        for uuid, task in ltask.COMPLETED.items():
            if task['entryDate'] < end and task['modifiedDate'] > start:
                tt = 0
                for time in task['times']:
                    if start < time[0] < end:
                        tt += (time[1] - time[0])
                for proj in task['projects']:
                    if cat == 'ndone' and proj in projects and types in ('both', 'project'):
                        append_proj(proj, [1, 1, tt])
                    elif cat != 'ndone' and types in ('both', 'project'):
                        append_proj(proj, [1, 1, tt])
                if not task['projects'] and types in ('both', 'task'):
                    if cat != 'ndone':
                        append_proj(task['title'], [1, 1, tt])

    def get_time_str(s):
        m = s // 60
        s -= m * 60
        h = m // 60
        m -= h * 60
        return "{:02}:{:02}".format(int(h), int(m))

    fmt_data = [5, 5, 6]
    for proj, data in projects.items():
        fmt_data[0] = max(fmt_data[0], len(proj))
        fmt_data[1] = max(fmt_data[1], len(get_time_str(data[2])))
        fmt_data[2] = max(fmt_data[2],
                          len("{:2.2f}%".format(100 * data[1] / data[0])))
    fmt_data.append(max(20, 80 - 6 - sum(fmt_data)))
    print("{}  {}  {}  {}".format(
        Attr("{:{}}".format("Title", fmt_data[0]), CONFIG.get_color('title')),
        Attr("{:{}}".format("Time", fmt_data[1]), CONFIG.get_color('title')),
        Attr("{:{}}".format("Perc", fmt_data[2]), CONFIG.get_color('title')),
        Attr("{:{}}".format("Progress", fmt_data[3]),
             CONFIG.get_color('title'))))
    for i, (proj, data) in enumerate(projects.items()):
        string = "\033[1m{:{}}\033[21m  {:>{}}  {:>{}.2f}%  {}".format(
            proj, fmt_data[0], get_time_str(data[2]), fmt_data[1],
            100 * data[1] / data[0], fmt_data[2] - 1,
            gen_progres_bar(fmt_data[3], data[1] / data[0]))
        if i % 2 == 1:
            print(Attr(string, CONFIG.get_color('background'), bg=True))
        else:
            print(string)
