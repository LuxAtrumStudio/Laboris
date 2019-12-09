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
            cdt += datetime.timedelta(days=dt[0],
                                      seconds=(3600 * dt[1]) + (60 * dt[2]) +
                                      dt[3])
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
            elif fmt.startswith("%A@") and arg.split("@")[0].lower() in (
                    'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
                    'friday', 'saturday'):
                name = arg.split("@")[0]
                cdt += datetime.timedelta(days=1)
                while cdt.strftime('%A').lower() != name.lower():
                    cdt += datetime.timedelta(days=1)
            elif fmt.startswith("%a@") and arg.split("@")[0].lower() in (
                    'sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'):
                name = arg.split("@")[0]
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
                        cdt.hour * 3600) + (cdt.minute *
                                            60) + cdt.second and cdt.hour < 12:
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

    if string[0] == 'T':
        string = string.replace('T', '@')
        string = "T" + string[1:]
    else:
        string = string.replace('T', '@')
    string = string.replace('/', '-')
    formats = [
        "%d-%m-%Y@%H:%M:%S", "%d-%m-%Y@%H:%M", "%d-%m-%Y@%H",
        "%m-%d-%Y@%H:%M:%S", "%m-%d-%Y@%H:%M", "%m-%d-%Y@%H",
        "%d-%m-%y@%H:%M:%S", "%d-%m-%y@%H:%M", "%d-%m-%y@%H", "%d-%m-%Y",
        "%m-%d-%Y", "%d-%m-%y", "%m-%d-%y", "%d-%m@%H:%M:%S", "%d-%m@%H:%M",
        "%d-%m@%H", "%m-%d@%H:%M:%S", "%m-%d@%H:%M", "%m-%d@%H", "%d-%m",
        "%m-%d", "%Y", "%d@%H:%M:%S", "%d@%H:%M", "%d@%H", "%d", "%H:%M:%S",
        "%H:%M", "%d-%m-%Y@%I:%M:%S%p", "%d-%m-%Y@%I:%M%p", "%d-%m-%Y@%I%p",
        "%m-%d-%Y@%I:%M:%S%p", "%m-%d-%Y@%I:%M%p", "%m-%d-%Y@%I%p",
        "%d-%m-%y@%I:%M:%S%p", "%d-%m-%y@%I:%M%p", "%d-%m-%y@%I%p",
        "%d-%m@%I:%M:%S%p", "%d-%m@%I:%M%p", "%d-%m@%I%p", "%m-%d@%I:%M:%S%p",
        "%m-%d@%I:%M%p", "%m-%d@%I%p", "%d@%I:%M:%S%p", "%d@%I:%M%p",
        "%d@%I%p", "%I:%M:%S%p", "%I:%M%p", "%A@%H:%M:%S", "%A@%H:%M", "%A@%H",
        "%A", "%a@%H:%M:%S", "%a@%H:%M", "%a@%H", "%a", "%A@%I:%M:%S%p",
        "%A@%I:%M%p", "%A@%I%p", "%a@%I:%M:%S%p", "%a@%I:%M%p", "%a@%I%p"
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
