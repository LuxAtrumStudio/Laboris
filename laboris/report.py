"""
Reports core structure for Laboris project
"""

from laboris.reports.list import list_report

def run_report(report = None):
    if report is None or report.lower() == "list":
        list_report()
