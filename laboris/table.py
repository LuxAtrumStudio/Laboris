import os
import ioterm.color as color
import ioterm.display as display
import math
from enum import Enum


class Table(object):

    class BoxFormat(Enum):
        NONE = 0
        ASCII = 1
        UNICODE = 2
        SPACE = 3

    def __init__(self):
        self.data = [[]]
        self.alignment = [[]]
        self.fmt = self.BoxFormat.NONE
        self.col_pri = False
        self.title_fmt = ["\033[1m", "\033[21m"]
        self.size_data = {"rows": 0, "cols": 0,
                          "max_width": 0, "max_height": 0, "col_size": list(), "width_add": 0, "total": 0}
        self.flags = {"zebra": False, "vert_sep": False, "horz_sep": False, "corner_sep": False,
                "title_row": list(), "title_col": list(), "same_width": False, "set_width": None, "min_height": 0}

    def update_alignment(self):
        if self.col_pri:
            tmp = [[''] * self.size_data["rows"] for _ in range(self.size_data["cols"])]
        else:
            tmp = [[''] * self.size_data["cols"] for _ in range(self.size_data["rows"])]
        for i, (a, b) in enumerate(zip(self.alignment, tmp)):
            for j, (c, d) in enumerate(zip(a, b)):
                if c:
                    tmp[i][j] = c
                else:
                    tmp[i][j] = d
        self.alignment = tmp

    def update_count(self):
        if self.col_pri:
            self.size_data["cols"] = len(self.data)
            for col in self.data:
                self.size_data["rows"] = max(self.size_data["rows"], len(col))
        else:
            self.size_data["rows"] = len(self.data)
            for row in self.data:
                self.size_data["cols"] = max(self.size_data["cols"], len(row))

    def update_col_size(self):
        self.size_data["col_size"] = [0] * self.size_data["cols"]
        if self.col_pri:
            for i, col in enumerate(self.data):
                for item in col:
                    self.size_data["col_size"][i] = max(self.size_data["col_size"][i], display.display_length(item))
        else:
            for row in self.data:
                for i, item in enumerate(row):
                    self.size_data["col_size"][i] = max(self.size_data["col_size"][i], display.display_length(item))
        if self.flags["same_width"] is True:
            max_width = max(self.size_data["col_size"])
            self.size_data["col_size"] = [max_width] * len(self.size_data["col_size"])


    def update_size(self):
        self.size_data["max_height"], self.size_data["max_width"] = os.popen(
            'stty size', 'r').read().split()
        self.size_data["max_height"] = int(self.size_data["max_height"])
        self.size_data["max_width"] = int(self.size_data["max_width"])
        if self.flags["set_width"] is not None and isinstance(self.flags["set_width"], int):
            self.size_data["max_width"] = self.flags["set_width"]
        self.update_count()
        self.update_col_size()
        if self.fmt == self.BoxFormat.NONE or self.flags["vert_sep"] is False:
            self.size_data["width_add"] = self.size_data["cols"] - 1
        elif self.fmt == self.BoxFormat.SPACE:
            self.size_data["width_add"] = (2 * (self.size_data["cols"] - 1))
        else:
            self.size_data["width_add"] = (
                3 * (self.size_data["cols"] - 1)) + 4
        if sum(self.size_data["col_size"]) + self.size_data["width_add"] > self.size_data["max_width"] or self.flags["set_width"] is not None:
            norm = [float(i) / (sum(self.size_data["col_size"]) +
                                self.size_data["width_add"]) for i in self.size_data["col_size"]]
            self.size_data["col_size"] = [
                int(math.floor(self.size_data["max_width"] * i)) for i in norm]
            while sum(self.size_data["col_size"]) + self.size_data["width_add"] > self.size_data["max_width"]:
                self.size_data["col_size"][-1] -= 1
        self.size_data["total"] = self.size_data["rows"] * \
            self.size_data["cols"]
        self.update_alignment()

    def vert(self, pos=1):
        ch = '|'
        if self.fmt == self.BoxFormat.NONE or self.flags["vert_sep"] is False:
            if pos == 1:
                print(' ', end='')
            if pos == 2:
                print()
            return
        elif self.fmt == self.BoxFormat.ASCII:
            ch = '|'
        elif self.fmt == self.BoxFormat.UNICODE:
            ch = '\u2502'
        elif self.fmt == self.BoxFormat.SPACE:
            ch = ''
            if pos == 0:
                return
            elif pos == 2:
                print()
                return
        if pos == 0:
            print('{} '.format(ch), end='')
        elif pos == 1:
            print(' {} '.format(ch), end='')
        elif pos == 2:
            print(' {}'.format(ch))

    def horz(self, pos=1):
        ch = '-'
        if self.fmt == self.BoxFormat.NONE or self.flags["horz_sep"] is False:
            return
        elif self.fmt == self.BoxFormat.ASCII:
            ch = '-'
        elif self.fmt == self.BoxFormat.UNICODE:
            ch = '\u2500'
        elif self.fmt == self.BoxFormat.SPACE:
            return
        has_vert = self.flags["vert_sep"] and self.fmt != self.BoxFormat.NONE
        if has_vert is False or self.flags["corner_sep"] is False:
            print(
                ch * (sum(self.size_data["col_size"]) + self.size_data["width_add"]))
        else:
            self.corner((pos * 3))
            for i, item in enumerate(self.size_data["col_size"]):
                print(ch * (item + 2), end='')
                if i != len(self.size_data["col_size"]) - 1:
                    self.corner((pos * 3) + 1)
            self.corner((pos * 3) + 2)
            print()

    def corner(self, pos=4):
        ch = '+'
        if self.fmt == self.BoxFormat.NONE:
            ch = ''
        elif self.fmt == self.BoxFormat.ASCII:
            ch = '+'
        elif self.fmt == self.BoxFormat.UNICODE:
            if pos == 0:
                ch = '\u250C'
            elif pos == 1:
                ch = '\u252C'
            elif pos == 2:
                ch = '\u2510'
            elif pos == 3:
                ch = '\u251C'
            elif pos == 4:
                ch = '\u253C'
            elif pos == 5:
                ch = '\u2524'
            elif pos == 6:
                ch = '\u2514'
            elif pos == 7:
                ch = '\u2534'
            elif pos == 8:
                ch = '\u2518'
        print(ch, end='')

    def display(self):
        self.update_size()
        self.horz(0)
        if self.col_pri:
            for j in range(max(self.size_data["rows"], self.flags["min_height"])):
                if self.flags["zebra"] is True and j % 2 != 0:
                    print(color.get_color(0, True), end='')
                self.vert(0)
                for i, col in enumerate(self.data):
                    if j < len(col):
                        color_attr  = None
                        if self.flags["zebra"] is True and j % 2 != 0:
                            color_attr = color.get_color(0, True)
                        item = display.print_aligned(col[j], self.alignment[i][j], self.size_data["col_size"][i], color_attr)
                        item = display.truncate(item, self.size_data["col_size"][i])
                        if i in self.flags["title_col"] or j in self.flags["title_row"]:
                            print(self.title_fmt[0], end='')
                        print(item, end='')
                        if self.flags["zebra"] is True and j % 2 != 0:
                            print(color.get_color(0, True), end='')
                        if i in self.flags["title_col"] or j in self.flags["title_row"]:
                            print(self.title_fmt[1], end='')
                        if i != self.size_data["cols"] - 1:
                            self.vert()
                    else:
                        print(' ' * self.size_data["col_size"][i], end='')
                        if i != self.size_data["cols"] - 1:
                            self.vert()
                self.vert(2)
                if self.flags["zebra"] is True and j % 2 != 0:
                    print(color.get_color('default', True), end='')
                if j != max(self.size_data["rows"], self.flags["min_height"]) - 1:
                    self.horz()

        else:
            for j, row in enumerate(self.data):
                if self.flags["zebra"] is True and j % 2 != 0:
                    print(color.get_color(0, True), end='')
                self.vert(0)
                for i, item in enumerate(row):
                    item = display.print_aligned(
                        item, self.alignment[j][i], self.size_data["col_size"][i])
                    item = display.truncate(item, self.size_data["col_size"][i])
                    if i in self.flags["title_col"] or j in self.flags["title_row"]:
                        print(self.title_fmt[0], end='')
                    print(item, end='')
                    if self.flags["zebra"] is True and j % 2 != 0:
                        print(color.get_color(0, True), end='')
                    if i in self.flags["title_col"] or j in self.flags["title_row"]:
                        print(self.title_fmt[1], end='')
                    if i != self.size_data["cols"] - 1:
                        self.vert()
                for i in range(len(row), self.size_data["cols"]):
                    print(' ' * self.size_data["col_size"][i], end='')
                    if i != self.size_data["cols"] - 1:
                        self.vert()
                self.vert(2)
                if self.flags["zebra"] is True and j % 2 != 0:
                    print(color.get_color("default", True), end='')
                if j != len(self.data) - 1 or self.flags["min_height"] > len(self.data):
                    self.horz()
            for j in range(len(self.data), self.flags["min_height"]):
                if self.flags["zebra"] is True and j % 2 != 0:
                    print(color.get_color(0, True), end='')
                self.vert(0)
                for i in range(self.size_data["cols"]):
                    print(' ' * self.size_data["col_size"][i], end='')
                    if i != self.size_data["cols"] - 1:
                        self.vert()
                self.vert(2)
                if self.flags["zebra"] is True and j % 2 != 0:
                    print(color.get_color("default", True), end='')
                if j != self.flags["min_height"] - 1:
                    self.horz()
        self.horz(2)

    def rotate_data(self):
        self.update_size()
        data_grid = list()
        for j, row in enumerate(self.data):
            data_grid.append([''] * self.size_data["cols"])
            for i, item in enumerate(row):
                data_grid[j][i] = item
        self.data = [list(i) for i in zip(*data_grid)]
        print(self.data)

    def row_add_attr(self, row, attr, attr_off="\033[0m"):
        for i, elem in enumerate(self.data[row]):
            self.data[row][i] = attr + elem + attr_off

    def col_add_attr(self, col, attr, attr_off="\033[0m"):
        for row in self.data:
            row[col] = attr + row[col] + attr_off

    def row_remove_attr(self, row, all=False):
        for i, elem in enumerate(self.data[row]):
            self.data[row][i] = display.no_attr(elem, all)

    def col_remove_attr(self, col, all=False):
        for row in self.data:
            row[col] = display.no_attr(row[col], all)

    def row_align(self, row, align):
        if isinstance(row, list):
            for r in row:
                self.row_align(r, align)
        else:
            self.update_size()
            if self.col_pri:
                for col in self.alignment:
                    col[row] = align
            else:
                for i, elem in enumerate(self.alignment[row]):
                    self.alignment[row][i] = align

    def col_align(self, col, align):
        if isinstance(col, list):
            for c in col:
                self.col_align(c, align)
        else:
            self.update_size()
            if self.col_pri:
                for i, elem in enumerate(self.alignment[col]):
                    self.alignment[col][i] = align
            else:
                for row in self.alignment:
                    row[col] = align
