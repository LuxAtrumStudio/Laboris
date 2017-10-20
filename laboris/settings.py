import laboris.theme as theme
import laboris.data as data

_theme = theme.Theme()
_pending = list()
_done = list()


def init():
    global _pending
    global _done
    _pending, _done = data.load_data()


def term():
    global _pending
    global _done
    data.save_data(_pending, _done)
