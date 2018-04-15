"""
    monitor.analyzer
    ~~~~~~~~~~~~~~~~

    A thread to parse logs for information, analyse it and store
    results.

    :copyright: None.
    :license: None
"""

import re

from follow import follow


def read_logs(filepath, traffic_summary):
    """
    Takes in the path to the log file, reads and keeps updating the
    traffic_summary based on the traffic_summary as soon as the data
    comes in.

    Parameters
    ----------
    filepath : str
        The absolute path of the log file
    traffic_summary: <TrafficSummary>
        An instance of ``Class <TrafficSummary>`` to store the logs

    Returns
    -------
    None
    """
    # the clf regex matches ip, any identifier, userid, time, request method,
    # URL, HTTP protocol, HTTP code, size of the returned data
    clf_regex = '([(\d\.)]+) (.*?) ([^\s]*?) \[(.*?)\] "([^\s]*?) ([^\s]*?) ([^\s]*?)" (\d+) (\d+)'
    compiled_regex = re.compile(clf_regex)

    logfile = open(filepath, "rb")
    lines = follow(logfile)

    for line in lines:

        # use regex, ignore if there was no match
        regex_match = compiled_regex.match(line)
        if regex_match is None:
            continue

        single_request = regex_match.groups()
        traffic_summary.update(single_request)
