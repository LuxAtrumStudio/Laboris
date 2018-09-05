"""
Laboris task manager CLI
"""

import laboris.api as api
import laboris.task as task

def main():
    print(api.HAS_ACCESS)
    api.check_network()
    print(api.HAS_ACCESS)
