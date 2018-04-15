# -*- coding: utf-8 -*-
"""
    monitor.monitor
    ~~~~~~~~~~~~~~~~

    A set of functions to parse and load configurations and initialize other
    components.

    :copyright: None.
    :license: None
"""

import json
import os
import traceback
from datetime import datetime


import util
from stats import TrafficSummary
from alerts import AlertHistory


def _check_config(configurations):
    """
    Takes in a a ``dictionary`` object and performs
    basic checks about data types, asserts type checks

    Parameters
    ----------
    configurations : dict
        The dictionary containing configuration file

    Returns
    -------
        None
    """

    # type check inputs
    for configuration in configurations:
        config_value = configurations[configuration]
        if configuration == "log_path":
            if not (type(config_value) == str or type(config_value) == unicode):
                print "Type Error in Configuration: ", configuration
                return False
        else:
            if not (type(config_value) == int or type(config_value) == float):
                print "Type Error in Configuration: ", configuration
                return False

    # check if the log path exits
    # configurations["log_path"] = os.path.join(util.LOGS_DIR,
    #                                          configurations["access_log_file"])
    if "log_path" not in configurations:
        print "Access log path does not exist."
        return False
    if not (os.path.exists(configurations["log_path"])):
        print "Access log path does not exist."
        return False

    return True


def load_config(config_path=util.CONFIG_FILE):
    """
    Takes in a path to a file and returns a dictionary containing
    configuration.

    Parameters
    ----------
    config_path : str
        The absolute or relative path of the configuration file

    Returns
    -------
    configs : dict
        The ``dictionary`` containing configurations
    success: bool
        A ``bool`` that states if loading was successful.
    """

    try:
        # load configuration file
        with open(config_path, 'rb') as config_file_stream:
            configs = json.load(config_file_stream)
        # check configurations for type errors
        success = _check_config(configs)
    except:
        traceback.print_exc()
        return None, False

    return configs, success


def init():
    """ Initialize the program state, load any previous state
     (if any), clears up the screen """

    # a hack to make strptime thread-safe (for older versions)
    datetime.strptime("2011-04-05 18:40:58.525996", "%Y-%m-%d %H:%M:%S.%f")

    # initialization
    util.clear_screen()
    traffic_summary = TrafficSummary()
    alert_history = AlertHistory()
    configs, success = load_config()
    return configs, traffic_summary, alert_history, success
