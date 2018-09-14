"""
Laboris color/attribute control
"""

ATTR_MAP = {
    'reset': ('\033[0m', '\033[0m'),
    'bold': ('\033[1m', '\033[21m'),
    'default': ('\033[39m', '\033[49m'),
    'black': ('\033[30m', '\033[40m'),
    'red': ('\033[31m', '\033[41m'),
    'green': ('\033[32m', '\033[42m'),
    'yellow': ('\033[33m', '\033[43m'),
    'blue': ('\033[34m', '\033[44m'),
    'magenta': ('\033[35m', '\033[45m'),
    'cyan': ('\033[36m', '\033[46m'),
    'light_grey': ('\033[37m', '\033[47m'),
    'dark_grey': ('\033[90m', '\033[100m'),
    'light_red': ('\033[91m', '\033[101m'),
    'light_green': ('\033[92m', '\033[102m'),
    'light_yellow': ('\033[93m', '\033[103m'),
    'light_blue': ('\033[94m', '\033[104m'),
    'light_magenta': ('\033[95m', '\033[105m'),
    'light_cyan': ('\033[96m', '\033[106m'),
    'white': ('\033[97m', '\033[107m'),
}


def GetAttr(attr_a, attr_b=None, attr_c=None, bg=False):
    if isinstance(attr_a, str):
        tmp = ""
        if isinstance(attr_b, str):
            tmp = GetAttr(attr_b, attr_c, bg=bg)
        if attr_a in ATTR_MAP:
            return tmp + (ATTR_MAP[attr_a][1] if bg else ATTR_MAP[attr_a][0])
        attr_a = attr_a.lstrip('#')
        rgb = tuple(int(attr_a[i:i + 2], 16) for i in (0, 2, 4))
        return tmp + "\033[{};2{};{};{}m".format(48 if bg else 38, rgb[0],
                                           rgb[1], rgb[2])
    elif isinstance(attr_a, float) and isinstance(attr_b, float) and isinstance(
            attr_c, float):
        rgb = tuple(int(attr_a * 255), int(attr_b * 255), int(attr_c * 255))
        return "\033[{};2{};{};{}m".format(48 if bg else 38, rgb[0],
                                           rgb[1], rgb[2])
    elif isinstance(attr_a, int) and isinstance(attr_b, int) and isinstance(
            attr_c, int):
        rgb = tuple(int(attr_a), int(attr_b), int(attr_c))
        return "\033[{};2{};{};{}m".format(48 if bg else 38, rgb[0],
                                           rgb[1], rgb[2])

def Attr(src, attr_a, attr_b=None, attr_c=None, bg=False):
    return GetAttr(attr_a, attr_b, attr_c, bg) + src + "\033[39;49m"
