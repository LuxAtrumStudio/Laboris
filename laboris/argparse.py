"""
Argument parsing module for Laboris
"""

import sys

def help():
    print("Usage: laboris TASK [action [options]]")
    print("       laboris REPORT")
    print("Laboris Task Manager(CLI) V2.0")
    print()
    print("  -h, --help     show list of command line options")

def parse():
    if '-h' in sys.argv or '--help' in sys.argv:
        help()
        exit(0)
    return None


