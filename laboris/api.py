"""
Laboris web API integration system
"""

import requests
import datetime

HAS_ACCESS = False
LAST_CHECKED = None

def check_network():
    global HAS_ACCESS, LAST_CHECKED
    if LAST_CHECKED is None or LAST_CHECKED + datetime.timedelta(hour=1) < datetime.datetime.now():
        LAST_CHECKED = datetime.datetime.now()
        try:
            requests.get('http://google.com', timeout=0.1)
            HAS_ACCESS = True
        except:
            HAS_ACCESS = False

def pull():
    check_network()
    if not HAS_ACCESS:
        return None
        # PULL WEB DATA
