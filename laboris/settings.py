import theme
import data

_theme = theme.Theme()
_pending = list()
_done = list()

def init():
    global _pending
    global _done
    _pending, _done = data.load_data()
