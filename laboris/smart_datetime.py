"""
Datetime reference system
"""

import datetime


def now():
    return datetime.datetime.now()


def new_timedelta(string):
    """
    Parses timedelta of the formats:
        [-+]DDTHH:MM:SS
        [-+]DDTHH:MM
        [-+]DDTHH
        [-+]HH:MM:SS
        [-+]HH:MM
        [-+]HH
        [-+]HHh
        [-+]MMm
        [-+]SSs
        [-+]DDd
    """

    def try_date_fmt(arg):
        dt = [0, 0, 0, 0]
        date = None
        time = None
        if arg[-1] == 'd':
            return [int(arg[:-1]), 0, 0, 0]
        elif arg[-1] == 's':
            return [0, 0, 0, int(arg[:-1])]
        elif arg[-1] == 'm':
            return [0, 0, int(arg[:-1]), 0]
        elif arg[-1] == 'h':
            return [0, int(arg[:-1]), 0, 0]
        elif 'T' in arg:
            arg = arg.split('T')
            date = arg[0]
            time = arg[1].split(':')
        else:
            time = arg.split(':')
        if date:
            try:
                dt[0] = int(date)
            except:
                return None
        for i, val in enumerate(time):
            try:
                dt[i + 1] = int(val)
            except:
                return None
        return dt

    string = string.replace('@', 'T')
    string = string.replace('/', '-')
    cdt = datetime.datetime.now().replace(microsecond=0)
    all_false = True
    for arg in string.split():
        dt = try_date_fmt(arg)
        if dt is not None:
            all_false = False
            cdt += datetime.timedelta(days=dt[0], seconds=(3600 * dt[1]) + (60 * dt[2]) + dt[3])
    if all_false:
        return None
    return cdt

def new_datetime(string):
    """
    Parses datetime of the formats:
        DD-MM-YYYYTHH:MM:SS
        DD-MM-YYYYTHH:MM
        DD-MM-YYYYTHH
        MM-DD-YYYYTHH:MM:SS
        MM-DD-YYYYTHH:MM
        MM-DD-YYYYTHH
        DD-MM-YYTHH:MM:SS
        DD-MM-YYTHH:MM
        DD-MM-YYTHH
        MM-DD-YYTHH:MM:SS
        MM-DD-YYTHH:MM
        MM-DD-YYTHH
        DD-MM-YYYY
        MM-DD-YYYY
        DD-MM-YY
        MM-DD-YY
        DD-MMTHH:MM:SS
        DD-MMTHH:MM
        DD-MMTHH
        MM-DDTHH:MM:SS
        MM-DDTHH:MM
        MM-DDTHH
        DD-MM
        MM-DD
        DD
        ATHH:MM:SS
        ATHH:MM
        ATHH
        A
        HH:MM:SS
        HH:MM
        yesterday
        tomorow
        last week
        next week
        last month
        next month
        last year
        next year
    """

    def try_date_fmt(arg, fmt):
        try:
            dt = datetime.datetime.strptime(arg, fmt)
            cdt = datetime.datetime.now().replace(microsecond=0)
            if fmt == '%A' and arg.lower() in ('sunday', 'monday', 'tuesday',
                                               'wednesday', 'thursday',
                                               'friday', 'saturday'):
                cdt += datetime.timedelta(days=1)
                while cdt.strftime('%A').lower() != arg.lower():
                    cdt += datetime.timedelta(days=1)
                return cdt.replace(hour=0, minute=0, second=0)
            elif fmt == '%a' and arg.lower() in ('sun', 'mon', 'tue', 'wed',
                                                 'thu', 'fri', 'sat'):
                cdt += datetime.timedelta(days=1)
                while cdt.strftime('%a').lower() != arg.lower():
                    cdt += datetime.timedelta(days=1)
                return cdt.replace(hour=0, minute=0, second=0)
            elif fmt.startswith("%AT") and arg.split("T")[0].lower() in (
                    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday'):
                name = arg.split("T")[0]
                cdt += datetime.timedelta(days=1)
                while cdt.strftime('%A').lower() != name.lower():
                    cdt += datetime.timedelta(days=1)
            elif fmt.startswith("%aT") and arg.split("T")[0].lower() in (
                    'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'):
                name = arg.split("T")[0]
                cdt += datetime.timedelta(days=1)
                while cdt.strftime('%a').lower() != name.lower():
                    cdt += datetime.timedelta(days=1)
            elif fmt == '%A' or fmt == '%a':
                return None

            if '%y' in fmt or "%Y" in fmt:
                cdt = cdt.replace(year=dt.year)
            if '%m' in fmt:
                cdt = cdt.replace(month=dt.month)
            if '%d' in fmt:
                cdt = cdt.replace(day=dt.day)
            if '%H' in fmt and '%p' not in fmt and cdt.date(
            ) == datetime.datetime.now().date():
                if (dt.hour * 3600) + (dt.minute * 60) + dt.second < (
                        cdt.hour * 3600) + (
                            cdt.minute * 60) + cdt.second and cdt.hour < 12:
                    dt = dt.replace(hour=dt.hour + 12)
            if '%H' in fmt or '%I' in fmt:
                cdt = cdt.replace(hour=dt.hour)
            else:
                cdt = cdt.replace(hour=0)
            if '%M' in fmt:
                cdt = cdt.replace(minute=dt.minute)
            else:
                cdt = cdt.replace(minute=0)
            if '%S' in fmt:
                cdt = cdt.replace(second=dt.second)
            else:
                cdt = cdt.replace(second=0)
            return cdt
        except ValueError:
            return None
        return None

    string = string.replace('@', 'T')
    string = string.replace('/', '-')
    formats = [
        "%d-%m-%YT%H:%M:%S", "%d-%m-%YT%H:%M", "%d-%m-%YT%H",
        "%m-%d-%YT%H:%M:%S", "%m-%d-%YT%H:%M", "%m-%d-%YT%H",
        "%d-%m-%yT%H:%M:%S", "%d-%m-%yT%H:%M", "%d-%m-%yT%H", "%d-%m-%Y",
        "%m-%d-%Y", "%d-%m-%y", "%m-%d-%Y", "%d-%mT%H:%M:%S", "%d-%mT%H:%M",
        "%d-%mT%H", "%m-%dT%H:%M:%S", "%m-%dT%H:%M", "%m-%dT%H", "%d-%m",
        "%m-%d", "%dT%H:%M:%S", "%dT%H:%M", "%dT%H", "%d", "%H:%M:%S", "%H:%M",
        "%d-%m-%YT%I:%M:%S%p", "%d-%m-%YT%I:%M%p", "%d-%m-%YT%I%p",
        "%m-%d-%YT%I:%M:%S%p", "%m-%d-%YT%I:%M%p", "%m-%d-%YT%I%p",
        "%d-%m-%yT%I:%M:%S%p", "%d-%m-%yT%I:%M%p", "%d-%m-%yT%I%p",
        "%d-%mT%I:%M:%S%p", "%d-%mT%I:%M%p", "%d-%mT%I%p", "%m-%dT%I:%M:%S%p",
        "%m-%dT%I:%M%p", "%m-%dT%I%p", "%dT%I:%M:%S%p", "%dT%I:%M%p", "%dT%I%p",
        "%I:%M:%S%p", "%I:%M%p", "%AT%H:%M:%S", "%AT%H:%M", "%AT%H", "%A",
        "%aT%H:%M:%S", "%aT%H:%M", "%aT%H", "%a", "%AT%I:%M:%S%p", "%AT%I:%M%p",
        "%AT%I%p", "%aT%I:%M:%S%p", "%aT%I:%M%p", "%aT%I%p"
    ]
    dt = None
    for fmt in formats:
        dt = try_date_fmt(string, fmt)
        if dt is not None:
            break
    return dt

def new(string):
    dt = new_datetime(string)
    if dt is None:
        return new_timedelta(string)
    return dt


