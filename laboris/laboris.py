"""
Laboris task manager CLI
"""

import laboris.api as api

def main():
    api.check_network()
    print("Hello World!");
