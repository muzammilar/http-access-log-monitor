"""
    monitor.follow
    ~~~~~~~~~~~~~~

    A python generator function that reads a file and returns the new lines
    added to it. Taken from David M. Beazley's source code and modified.

    :author: David M. Beazley
    :copyright: 2008 David M. Beazley.
    :license: unknown
    :src: http://www.dabeaz.com/generators/follow.py

"""

import time

import util


def follow(filestream):
    """
    A `generator` function that reads a file and returns the new lines added to it.

    Parameters
    ----------
    filestream : input stream
        The IO stream of the file to be read

    Returns
    -------
    line : str (yield)
        The single line containing new data found in the file
    """

    # go to the last line before the end of file
    # see: https://docs.python.org/2/tutorial/inputoutput.html
    filestream.seek(0, 2)

    while True:
        line = filestream.readline()
        if not line:
            time.sleep(0.5)  # sleep if nothing is available
            continue
        yield line
