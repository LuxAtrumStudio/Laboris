CSI = '\003['


def code_to_char(code):
    return CSI + str(code) + 'm'


class Color(object):
    def __init__(self, color):
        self.ESC = "\033["
        self.END = "m"
        self.color = color
        self.paint = {
            "black": 0,
            "red": 1,
            "green": 2,
            "yellow": 3,
            "blue": 4,
            "magenta": 5,
            "cyan": 6,
            "light_gray": 7,
            "dark_gray": 8,
            "light_red": 9,
            "light_green": 10,
            "light_yellow": 11,
            "light_blue": 12,
            "light_magenta": 13,
            "light_cyan": 14,
            "white": 15
        }
        self.reserve_paint = dict()

    def attribute(self):
        paint = {
            "bold": self.ESC + "1" + self.END,
            1: self.ESC + "1" + self.END,
            "dim": self.ESC + "2" + self.END,
            2: self.ESC + "2" + self.END,
            "underlined": self.ESC + "4" + self.END,
            4: self.ESC + "4" + self.END,
            "blink": self.ESC + "5" + self.END,
            5: self.ESC + "5" + self.END,
            "reverse": self.ESC + "7" + self.END,
            7: self.ESC + "7" + self.END,
            "hidden": self.ESC + "8" + self.END,
            8: self.ESC + "8" + self.END,
            "reset": self.ESC + "0" + self.END,
            0: self.ESC + "0" + self.END,
            "res_bold": self.ESC + "21" + self.END,
            21: self.ESC + "21" + self.END,
            "res_dim": self.ESC + "22" + self.END,
            22: self.ESC + "22" + self.END,
            "res_underlined": self.ESC + "24" + self.END,
            24: self.ESC + "24" + self.END,
            "res_blink": self.ESC + "25" + self.END,
            25: self.ESC + "25" + self.END,
            "res_reverse": self.ESC + "27" + self.END,
            27: self.ESC + "27" + self.END,
            "res_hidden": self.ESC + "28" + self.END,
            28: self.ESC + "28" + self.END,
        }
        return paint[self.color]

    def foreground(self):
        code = self.ESC
        if str(self.color).isdigit():
            self.reverse_dict()
            color = self.reserve_paint[str(self.color)]
            val = int(self.paint[self.color])
            if val > 7:
                val += 82
            else:
                val += 30

            return code + str(val) + self.END
        else:
            val = int(self.paint[self.color])
            if val > 7:
                val += 82
            else:
                val += 30
            return code + str(val) + self.END

    def background(self):
        code = self.ESC
        if str(self.color).isdigit():
            self.reverse_dict()
            color = self.reserve_paint[str(self.color)]
            val = int(self.paint[self.color])
            if val > 7:
                val += 92
            else:
                val += 40
            return code + str(val) + self.END
        else:
            val = int(self.paint[self.color])
            if val > 7:
                val += 92
            else:
                val += 40
            return code + str(val) + self.END

    def reverse_dict(self):
        self.reserve_paint = dict(zip(self.paint.values(), self.paint.keys()))


def attr(color):
    """alias for colored().attribute()"""
    return Color(color).attribute()


def fg(color):
    """alias for colored().foreground()"""
    return Color(color).foreground()


def bg(color):
    """alias for colored().background()"""
    return Color(color).background()


def stylize(text, styles, reset=True):
    """conveniently styles your text as and resets ANSI codes at its end."""
    terminator = attr("reset") if reset else ""
    return "{}{}{}".format("".join(styles), text, terminator)
