import json


class Theme:

    def __init__(self):
        self.colors = dict()
        self.background = list()
        self.color_16_mill = False
        self.color_256 = False
        self.get_color_support()

    def get_color_support(self):
        """
        Gets the color support that the current terminal can support. Either 16 million, 256, or 8.
        """
        self.color_16_mill = True
        self.color_256 = True

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
        color = {
            "black": 0,
            "red": 1,
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
            self.background = obj["background"]
            del obj["background"]
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

    def set_color(self, color):
        print(self.get_color(color), end='')
