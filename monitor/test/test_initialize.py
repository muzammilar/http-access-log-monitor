# -*- coding: utf-8 -*-
"""
    monitor.test.test_initialize
    ~~~~~~~~~~~~~~~~

    A set of tests for monitor.initialize.

    :copyright: None.
    :license: None
"""

from monitor import initialize

class TestInitialze:

    def test_empty_config(self):
        # empty config
        assert(initialize._check_config({}) is False)

    def test_valid_log(self):
        # valid path
        assert (initialize._check_config({"log_path": "requirements.txt"}) is True)

    def test_invalid_log(self):
        # invalid valid path
        assert (initialize._check_config({"log_path": "emptiness.file"}) is False)
