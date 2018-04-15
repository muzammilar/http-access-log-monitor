"""
    monitor.monitor
    ~~~~~~~~~~~~~~~~

    A simple console system to monitor HTTP access logs.

    :copyright: None.
    :license: None
"""

import sys
import threading
import signal
import time

import initialize
import analyzer
import alerts


def close_program(graceful_close):
    """A function to close threads and exit the program"""

    # send a system wide signal to close
    if not graceful_close:
        sys.exit(1)
    """
    for thread in _RUNNING_PROCESSES:
        try:
            if not thread.isAlive():
                continue
            thread.join()
        except:
            pass
    """


def signal_handler_close(signal, frame):
    close_program(False)


def main():
    """ The entry point of the system """

    # set up signal handlers
    signal.signal(signal.SIGINT, signal_handler_close)
    signal.signal(signal.SIGTERM, signal_handler_close)

    # initialize
    configs, traffic_summary, alert_history, success = initialize.init()
    program_running = True
    running_processes = []
    if not success:
        print "Failed to initialize the program."
        sys.exit(1)

    # start log parser thread
    logger_thread = threading.Thread(target=analyzer.read_logs,
                                     args=(configs["log_path"], traffic_summary,))
    running_processes.append(logger_thread)

    # create alerts thread
    alert_thread = threading.Thread(target=alerts.create_alert,
                                    args=(configs, alert_history, traffic_summary,))
    running_processes.append(alert_thread)

    # start all threads
    for thread in running_processes:
        thread.daemon = True
        thread.start()

    try:
        # update the display and stats on the console
        while program_running:
            traffic_summary.print_traffic_summary_periodic(alert_history)
            time.sleep(configs["sleep_proc_update_scrs"])

    except KeyboardInterrupt:
        program_running = False
        close_program(False)
    except: # generic exception
        close_program(False)


if __name__ == "__main__":
    main()
