"""
User prompt module
"""

from enum import IntFlag, Enum
from laboris.getch import getch
from laboris.fuzz import fuzz


class pmt(IntFlag):
    ECHO = 1
    PASSWORD = 2
    NUMBER = 4
    FLOAT = 8
    VERTICAL = 16
    HORIZONTAL = 32


class se(IntFlag):
    NUMBER = 1


def yn_choice(msg,
              default=None,
              style=None,
              suggestion_style=None,
              default_style=None):
    if style is None:
        style = ""
    if suggestion_style is None:
        suggestion_style = style
    if default_style is None:
        default_style = suggestion_style
    print(
        "{}\033[0m {}(Y/N)\033[0m{}: {}".format(msg, suggestion_style, (
            "{}[Y]\033[0m".format(default_style) if default is True else
            ('{}[N]\033[0m'.format(default_style) if default is False else "")),
                                                style),
        end='',
        flush=True)
    while True:
        ch = getch()
        if ch in ('y', 'Y', '1', 't', 'T'):
            print('True\033[0m')
            return True
        elif ch in ('n', 'N', '0', 'f', 'F'):
            print('False\033[0m')
            return False
        elif ord(ch) == 13 and default is not None:
            print(('True\033[0m' if default is True else 'False\033[0m'))
            return default


def select(msg,
           options=None,
           select_style="\033[1m",
           default=0,
           flags=se.NUMBER):
    print("{}{}".format(msg, "\033[0m"))
    i = default
    number = flags & se.NUMBER
    while True:
        for j, x in enumerate(options):
            if j == i:
                print("{}{}{}{}".format(select_style, '{}: '.format(j) if number else '', x, "\033[0m"))
            else:
                print("{}{}{}".format("{}: ".format(j) if number else '', x, "\033[0m"))
        ch = getch()
        if ord(ch) == 13:
            break
        elif ord(ch) == 66:
            i = (i + 1) % len(options)
        elif ord(ch) == 65:
            i = (i - 1) % len(options)
        elif number:
            if 48 <= ord(ch) <= 58 and ord(ch) - 48 < len(options):
                i = ord(ch) - 48
        for x in options:
            print("\033[A\033[2K\033[G", end='')
    for x in options:
        print("\033[A\033[2K\033[G", end='')
    print("\033[2Z\033[A\033[2Z\033[G{}{}{}".format(msg, "\033[0m", options[i]))
    return i


def prompt(msg,
           options=None,
           style=None,
           suggestion_style=None,
           select_style=None,
           suggestion_n=5,
           flags=pmt.ECHO | pmt.HORIZONTAL):
    print("{}{}{}".format(msg, "\033[0m", style), end='', flush=True)
    if style is None:
        style = ""
    if suggestion_style is None:
        suggestion_style = style
    if select_style is None:
        select_style = suggestion_style
    usr_input = ""
    sug_input = ""
    echo = flags & pmt.ECHO
    password = flags & pmt.PASSWORD
    horizontal = flags & pmt.HORIZONTAL
    is_number = False
    is_float = False
    has_decimal = False

    def eprint(ch):
        if echo and password:
            print("*", end='', flush=True)
        elif echo:
            print(ch, end='', flush=True)

    i = -1
    ch = ' '
    suggestions = []
    while ord(ch) != 13:
        if i == -1 and options:
            suggestions = fuzz(usr_input, options, size=suggestion_n)
        if suggestions:
            if horizontal:
                print(
                    "\n\033[2K{}\033[A\033[G".format(" ".join([
                        "{}{}{}".format(
                            (select_style if i == j else suggestion_style), x,
                            "\033[0m") for j, x in enumerate(suggestions)
                    ])),
                    end='',
                    flush=True)
        print(
            "\033[G\033[2K{}{}{}\033[0m".format(
                msg, style, (usr_input if i == -1 else suggestions[i])),
            end='',
            flush=True)
        ch = getch()
        if ord(ch) in (0, 13, 27):
            break
        elif ord(ch) == 9:
            i += 1
            if i >= len(suggestions):
                i = -1
        elif ord(ch) == 127:
            if i != -1:
                usr_input = suggestions[i]
                i = -1
            if is_float and usr_input[-1] in ('.', ','):
                has_decimal = False
            usr_input = usr_input[:-1]
            print("\033[D \033[D", end='', flush=True)
        else:
            if i != -1:
                usr_input = suggestions[i]
                i = -1
            if is_number and 48 <= ord(ch) <= 57:
                usr_input += ch
                eprint(ch)
            elif is_float and 48 <= ord(ch) <= 57:
                usr_input += ch
                eprint(ch)
            elif is_float and not has_decimal and ch in ('.', ','):
                has_decimal = True
                usr_input += ch
                eprint(ch)
            elif not is_number and not is_float:
                usr_input += ch
                eprint(ch)

    if suggestions:
        if horizontal:
            print("\n\033[G\033[2K", end='', flush=True)
    else:
        print()
