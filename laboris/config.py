"""
Laboris config parsing, and generation
"""

import colorsys
import json
import os
from math import inf
from laboris import color as col
from laboris import prompt as pmt


class Settings(object):

    def __init__(self):
        self.theme = {}

    def gen_gradient(self, a, b, t):

        def angle_diff_min(s, e):
            cw = e - s if s <= e else 360.0 + e - s
            ccw = e - s if e <= s else -360.0 - s + e
            return ccw if abs(cw) > abs(ccw) else cw

        a = a[1:]
        b = b[1:]
        start_rgb = tuple(int(a[i:i + 2], 16) for i in (0, 2, 4))
        start = colorsys.rgb_to_hsv(start_rgb[0], start_rgb[1], start_rgb[2])
        end_rgb = tuple(int(b[i:i + 2], 16) for i in (0, 2, 4))
        end = colorsys.rgb_to_hsv(end_rgb[0], end_rgb[1], end_rgb[2])
        # print(start, end)
        dh = angle_diff_min(start[0], end[0])
        ds = end[1] - start[1]
        dv = end[2] - start[2]
        return colorsys.hsv_to_rgb((dh * t) + start[0], (ds * t) + start[1],
                                   (dv * t) + start[2])

    def get_color(self, path, value=None, obj=None):
        if isinstance(path, str):
            return self.get_color(path.split('.'), value)
        elif not path:
            if value is None:
                return obj
            for key, val in obj.items():
                if '-' in key:
                    start, end = map(float, key.split('-'))
                elif key.endswith('+'):
                    start = float(key.split('+')[0])
                    end = inf
                    value = start
                if start <= value < end:
                    if len(val) == 2 and val[0].startswith(
                            '#') and val[1].startswith('#'):
                        return self.gen_gradient(
                            val[0], val[1], (value - start) / (end - start))
                    else:
                        return val
        elif obj and path[0] in obj:
            return self.get_color(path[1:], value, obj[path[0]])
        elif path[0] in self.theme:
            return self.get_color(path[1:], value, self.theme[path[0]])


CONFIG = Settings()


def load_config():
    global CONFIG
    if os.path.isfile(os.path.expanduser("~/.config/laboris/config.json")):
        data = json.load(
            open(os.path.expanduser("~/.config/laboris/config.json")))
        CONFIG.theme = data['theme']
    else:
        generate()


def save_config():
    if not os.path.exists(os.path.expanduser('~/.config/laboris')):
        os.makedirs(os.path.expanduser('~/.config/laboris'))
    data = {'theme': CONFIG.theme}
    json.dump(data,
              open(os.path.expanduser('~/.config/laboris/config.json'), 'w'))


def generate():
    global CONFIG
    CONFIG = Settings()
    print(col.Title('Generate Config'))
    print(col.SubTitle("Options"))
    if pmt.yn_choice(
            col.Attr('Generate Theme', 'magenta', 'bold'),
            default=True,
            style=col.GetAttr('bold'),
            suggestion_style=col.GetAttr('cyan', 'bold'),
            default_style=col.GetAttr('yellow', 'bold')):
        CONFIG.theme = {
            'background': 'black',
            'title': ['white', 'bold', 'underline'],
            "components": {
                'project': ['cyan'],
                'tags': ['yellow']
            },
            'msgs': {
                'success': ['green', 'bold'],
                'warning': ['yellow', 'bold'],
                'error': ['red', 'bold'],
            },
            'action': {
                'add': ['blue'],
                'complete': ['green'],
                'delete': ['red'],
                'start': ['yellow'],
                'stop': ['yellow']
            },
            'status': {
                'active': [['black'], ['green']],
                'overdue': [['black'], ['red']],
                'due-today': [['red'], ['yellow']]
            },
            'urgency': {
                '0-3': ['#2196f3', '#6caf50'],
                '3-10': ['#6caf50', '#f44336'],
                '10+': ['#f44336', 'bold']
            }
        }
    save_config()
