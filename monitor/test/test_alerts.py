# -*- coding: utf-8 -*-
"""
    monitor.test.test_alerts
    ~~~~~~~~~~~~~~~~

    A set of tests for monitor.alerts.

    :copyright: None.
    :license: None
"""

from monitor.alerts import AlertMonitor, AlertHistory


class TestAlerts:

    def test_queue_size_max(self):
        """ check the queue size"""

        # basic test
        # 2 minutes window, with 60 second interval
        alert = AlertMonitor(100, 2, 60)
        assert(alert.queue_size_max == 2)

        # 2 minutes window, with 5 second interval
        alert = AlertMonitor(100, 2, 5)
        assert(alert.queue_size_max == 24)

        # if the threshold window is smaller than sleep time
        alert = AlertMonitor(100, 1, 100)
        assert (alert.queue_size_max == 1)

    def test_raise_alert(self):
        """ check an alert is raised or not"""

        # check if value stays below threhold, no alert should be raised
        # queue size will be 2 here.
        alert = AlertMonitor(100, 2, 60)
        alert_history = AlertHistory()

        for iter_i in xrange(100):
            alert._update_queue(45)

        alert._raise_alert(alert_history)

        assert (len(alert_history._alert_history) == 0)

        # corner case - exact 100
        alert._update_queue(50)   # 50
        alert._update_queue(50)   # 50
        alert._raise_alert(alert_history)

        assert (len(alert_history._alert_history) == 0)

        # check if alert is raised, alert should be raised
        alert._update_queue(65)   # 65+50 = 115
        alert._raise_alert(alert_history)

        assert (len(alert_history._alert_history) == 1
                and alert_history._alert_history[0].startswith("High traffic "
                                                               "generated an alert "
                                                               "- hits = 115"))

        # no NEW alert should be triggered when more data added
        alert._update_queue(135)   # 65+135 = 200
        alert._raise_alert(alert_history)
        assert (len(alert_history._alert_history) == 1)


    def test_alert_silence(self):
        """ Tests if alert cancelation works for corner case -ie thresh"""

        alert = AlertMonitor(100, 2, 60)
        alert_history = AlertHistory()

        # no cancellation as value is still lower
        for iter_i in xrange(100):
            alert._update_queue(2)

        alert._cancel_alert(alert_history)
        assert (len(alert_history._alert_history) == 0)


        # simulate an alert
        alert.alert_triggered = True
        for iter_i in xrange(100):
            alert._update_queue(55)

        # alert should not be cancelled as value is still higher
        alert._cancel_alert(alert_history)
        assert (len(alert_history._alert_history) == 0)

        # cancel alert
        alert._update_queue(2)

        alert._cancel_alert(alert_history)
        assert (len(alert_history._alert_history) == 1
                and alert_history._alert_history[0].startswith("Alert recovered"))


    def test_alert_silence_thresh(self):
        """ Tests if alert cancelation works for corner case -ie thresh"""

        alert = AlertMonitor(100, 2, 60)
        alert_history = AlertHistory()

        # simulate an alert
        alert.alert_triggered = True
        for iter_i in xrange(100):
            alert._update_queue(55)

        # alert should not be cancelled as value is still higher
        alert._cancel_alert(alert_history)
        assert (len(alert_history._alert_history) == 0)

        # corner case
        alert._update_queue(50)
        alert._update_queue(50)

        alert._cancel_alert(alert_history)
        assert (len(alert_history._alert_history) == 1
                and alert_history._alert_history[0].startswith("Alert recovered"))


