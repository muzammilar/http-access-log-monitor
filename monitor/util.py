# -*- coding: utf-8 -*-
"""
    monitor.util
    ~~~~~~~~~~~~~~~~

    A file to contain basic directory names, files, shared locks, etc.

    :copyright: None.
    :license: None
"""

import os
import platform


_CODE_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(_CODE_ROOT_DIR)
#LOGS_DIR = os.path.join(PROJECT_DIR, "logs")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config.json")


def clear_screen():
    """ Clears the console """
    # added cross-platform support for Windows client.
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

