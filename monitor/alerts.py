# -*- coding: utf-8 -*-
"""
    monitor.alerts
    ~~~~~~~~~~~~~~~~

    A file to generate alerts in the system.

    :copyright: None.
    :license: None
"""
import threading
import time
from Queue import Queue
from datetime import datetime


class AlertHistory:
    """A class to store the informantion about when an alert was triggered and
     and when it returned to original state. This is a class that
     will store all the alerts for the system to display"""

    def __init__(self):
        self._lock_history = threading.Lock()
        self._alert_history = []

    def add_alert(self, alert_str):
        with self._lock_history:
            self._alert_history.append(alert_str)

    def print_alerts(self):
        with self._lock_history:
            for alert in self._alert_history:
                print alert


class AlertMonitor:
    """ A class containing the state information regarding an alert
        This class will not store all the historical alerts.
        Uses a queue structure on a discrete (not continuous) interval
        to get the average hits
    """

    def __init__(self, thresh, thresh_time_min, sleep_time):

        self.alert_triggered = False
        self.threshold = thresh
        self.thresh_time_sec = thresh_time_min * 60  # minutes to seconds
        self.value = 0       # stores the number of hits for alert
        self.total_hits = 0  # stores the number of hits between the sleep intvl

        # create a queue to store all the summary stats
        self.queue_size_max = int((self.thresh_time_sec * 1.0) / sleep_time)
        if self.queue_size_max < 1:  # it's possible for time errors
            self.queue_size_max = 1
        self.queue = Queue(maxsize=self.queue_size_max)

    def update(self, traffic_summary, alert_history):
        """ Takes in traffic_summary, compares with the previous
        number of pages visited (hits), then see if an alert should be generated
        or not. Then raises an alert or cancels one"""

        new_total_hits = traffic_summary.get_total_hits()
        interval_hits = new_total_hits - self.total_hits   # hits during the time interval
        self.total_hits = new_total_hits

        # update the queue
        self._update_queue(interval_hits)

        # raise alert if neeeded
        self._raise_alert(alert_history)

        # cancel a raised alert if needed
        self._cancel_alert(alert_history)

    def _update_queue(self, interval_hits):
        """ Updates the queue storing the hits information
        Add the interval hits to queue and remove something if need """

        # remove something if need
        if self.queue.full():
            self.value -= self.queue.get()  # remove an element

        # add the new value to the queue
        self.value += interval_hits
        self.queue.put(interval_hits)

    def _raise_alert(self, alert_history):
        """ Raise alert if not already raised """

        if self.value > self.threshold and (not self.alert_triggered):
            alert_str = "High traffic generated an alert - hits = " \
                        + str(self.value) + " at time " \
                        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alert_history.add_alert(alert_str)
            self.alert_triggered = True

    def _cancel_alert(self, alert_history):
        """ Cancel an alert if already raised """

        if self.value <= self.threshold and self.alert_triggered:
            alert_str = "Alert recovered - hits = " + \
                        str(self.value) + " at time " \
                        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alert_history.add_alert(alert_str)
            self.alert_triggered = False


def create_alert(configs, alert_history, traffic_summary):
    """
    This is the thread that executes and checks for any anomalies in traffic.

    Parameters
    ----------
    configs : dict
        The dictionary containing configuration file
    alert_history : <AlertHistory>
            An instance of the ``Class <AlertHistory>`` containing
            all the historical alerts generated/recovered.
    traffic_summary: <TrafficSummary>
        An instance of ``Class <TrafficSummary>`` to store the logs

    """

    thread_running = True
    alert_monitor = AlertMonitor(configs["traffic_threshold"],
                                 configs["traffic_threshold_time_m"],
                                 configs["sleep_proc_threshold"])
    while thread_running:
        alert_monitor.update(traffic_summary, alert_history)
        time.sleep(configs["sleep_proc_threshold"])
