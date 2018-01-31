import os
import json
from enum import Enum


class Theme:

    def __init__(self):
        self.colors = dict()
        self.background = list()
        self.color_16_mill = False
        self.color_256 = False
        self.get_color_support()

    class ColorAccess(Enum):
        NO_COLOR = 0
        COLOR_8_BIT = 1
        COLOR_16_BIT = 2
        COLOR_256_BIT = 3
        COLOR_TRUE = 4

    def clamp(self, n, minn, maxn):
        if n < minn:
            return minn
        elif n > maxn:
            return maxn
        return n

    def get_color_support(self):
        """
        Gets the color support that the current terminal can support. Either 16 million, 256, or 8.
        """
        self.color_16_mill = True
        self.color_256 = True

    def get_color_ability(self):
        if "COLORTRM" in os.environ:
            env = os.environ["COLORTERM"]
            if env == "truecolor":
                return self.ColorAccess.COLOR_TRUE
        if "TERM" in os.environ:
            term = os.environ["TERM"]
            if term == "xterm":
                return self.ColorAccess.COLOR_256_BIT
            elif term == "xterm-256color":
                return self.ColorAccess.COLOR_TRUE
            elif term == "linux":
                return self.ColorAccess.COLOR_16_BIT
        if "CI" in os.environ:
            cis = os.environ["CI"]
            if cis == "travis":
                return self.ColorAccess.COLOR_16_BIT
        return self.ColorAccess.NO_COLOR

    def get_color_format(self, color):
        if type(color) is list:
            if type(color[0]) is tuple:
                return 2
            elif type(color[0]) is int:
                return 1
            else:
                return 0
        else:
            return 0

    def get_color_name(self, color):
        colors = {'black': 0, 'red': 1, 'green': 2, 'yellow': 3, 'blue': 4, 'magenta': 5, 'cyan': 6, 'light_grey': 7, 'dark_grey': 8,
                  'light_red': 9, 'light_green': 10, 'light_yellow': 11, 'light_blue': 12, 'light_magenta': 13, 'light_cyan': 14, 'white': 15}
        if color in colors:
            return colors[color]
        return None

    def reset(self):
        return "\033[0m"

    def reset_cmd(self):
        print("\033[0m", end='')

    def bg(self):
        if type(self.background) is list:
            return "\033[48;2;{};{};{}m".format(
                self.background[0], self.background[1], self.background[2])
        elif type(self.background) is int:
            return "\033[{}m".format(self.background)
        else:
            return str()

    def parse_json(self, obj, index=str()):
        if "background" in obj:
            self.background = obj["background"]
            del obj["background"]
        color = {
            "black": [30, 40],
            "red": [31, 41],
            "green": [32, 42],
            "yellow": [33, 43],
            "blue": [34, 44],
            "magenta": [35, 45],
            "cyan": [36, 46],
            "grey": [37, 47]
        }
        for key, value in obj.items():
            if type(value) is dict:
                self.parse_json(value, index + key + '.')
            else:
                for i, item in enumerate(value):
                    if type(item) is str:
                        value[i] = color[item]
                self.colors[index + key] = value

    def parse_file(self, file_path):
        with open(file_path) as json_file:
            obj = json.load(json_file)
            self.parse_json(obj)

    def get_key(self, color):
        while color not in self.colors.keys() and color != str():
            color = ".".join(color.split('.')[1:])
        if color == str():
            return False
        return color

    def get_color(self, color):
        _str = str()
        if self.get_key(color) is not False:
            color = self.get_key(color)
            if self.color_16_mill is True and self.get_color_format(
                    self.colors[color]) == 2:
                if self.colors[color][0] is not None and self.colors[color][0] != -1:
                    _str += "\033[38;2;{};{};{}m".format(
                        self.colors[color][0][0], self.colors[color][0][1],
                        self.colors[color][0][2])
                if self.colors[color][1] is not None and self.colors[color][1] != -1:
                    _str += "\033[48;2;{};{};{}m".format(
                        self.colors[color][1][0], self.colors[color][1][1],
                        self.colors[color][1][2])
            if self.color_256 is True and self.get_color_format(
                    self.colors[color]) == 1:
                if self.colors[color][0] is not None and self.colors[color][0] != -1:
                    _str += "\033[{}m".format(self.colors[color][0])
                if self.colors[color][1] is not None and self.colors[color][1] != -1:
                    _str += "\033[{}m".format(self.colors[color][1])
            if len(self.colors[color]) > 2:
                for attr in self.colors[color][2:]:
                    _str += "\033[{}m".format(attr)
        return _str

    def get_color_escape(self, color, background=False):
        access = self.get_color_ability()
        if isinstance(color, str):
            if color.lower() == "default":
                if background is False:
                    return "\033[39m"
                return "\033[49m"
            elif self.get_color_name(color) is not None:
                color = self.get_color_name(color)
            else:
                color = color.lstrip('#')
                if color == str():
                    color = "ffffff"
                color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
        if isinstance(color, list):
            color = tuple(color)
        if isinstance(color, tuple):
            red, green, blue = color
            red = self.clamp(red, 0, 256)
            green = self.clamp(green, 0, 256)
            blue = self.clamp(blue, 0, 256)
            if access is self.ColorAccess.COLOR_256_BIT:
                red = ((red / 256) * 5)
                green = ((green / 256) * 5)
                blue = ((blue / 256) * 5)
                xterm = (36 * int(round(red))) + (6 * int(round(green))) + (int(
                    round(blue))) + 16
                if background is False:
                    return "\033[38;5;{}m".format(xterm)
                return "\033[48;5;{}m".format(xterm)
            if background is False:
                return "\033[38;2;{};{};{}m".format(red, green, blue)
            return "\033[48;2;{};{};{}m".format(red, green, blue)
        if isinstance(color, int):
            color = self.clamp(color, 0, 256)
            if background is False:
                return "\033[38;5;{}m".format(color)
            return "\033[48;5;{}m".format(color)
        return str()

    def set_color(self, color):
        print(self.get_color(color), end='')
