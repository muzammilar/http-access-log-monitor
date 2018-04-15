 

HTTP Log Monitor
================

##### Muzammil Abdul Rehman

 

### Instructions:

-   The source code is written in Python2.

-   **Setup:** Create a `virtualenv` and run `pip install -r requirements.txt`

-   **Starting the Monitor:** To start the program, `cd` in to the
    `log-monitor/monitor` directory and run `python monitor.py`

-   **Running Tests:** To run the tests for the alerts (and some other tests),
    cd in to the `log-monitor` directory and run `pytest --pyargs monitor`

-   **Config File**: The configuration file is present in the `log-monitor`
    directory as `config.json`. All these values must be specified in the c It
    contains the following values:

    -   `sleep_proc_update_scrs` : This is the time interval to update the
        display of the console, default is 10 seconds.

    -   `sleep_proc_threshold` : This is the time interval for the Alerts thread
        (below) to update results.

    -   `traffic_threshold_time_m` : This the time period in minutes that is
        monitored before current time to check if threshold is crossed. Current
        value is 2, i.e. 2 minutes.

    -   \`traffic_threshold\`: This is the traffic threshold that when crossed
        causes an alert. Current value is 20 i.e. 20 hits per 2 minutes (if
        above value is 2 minutes).

 

### Overview:

-   The program has 3 threads with each having a specific purpose; log parse and
    analysis, alerts, and display.

    -   **Log Parse and Analysis thread:** This thread parses the log file for
        information using a generator function (to keep track of the latest line
        read), then uses regex to parse each line of the access log. It then
        gets the HTTP protocol, the server codes, data size, etc, and it for the
        user. Only the aggregate information is stored by this thread. No
        information about the individual line in the access log is stored (only
        aggregate).

    -   **Alerts:** This thread monitors the traffic and sees if the threshold
        is crossed over the time period. It uses a `Queue` data structure to
        store change in traffic at *discrete intervals* (i.e every 5 seconds,
        can be changed to any number). It does not store every request for the
        past 2 minutes but only the aggregate at intervals. Once the threshold
        is crossed, it triggers an alert and once it comes back, the alert is
        recalled.

    -   **Display:** This thread displays and updates the console with alerts
        and system stats, every 10 seconds.

 

-   The locks used in the system are in cases where absolutely necessary (thanks
    to GIL).

-   All the functions are heavily documented.

-   This system has *cross-platform* support, supporting both Unix and Windows
    based consoles.

-   To generate logs, I used a customized version of the
    ‘https://github.com/kiritbasu/Fake-Apache-Log-Generator\`project.

 

### Improvements:

There are few things that can be improved in the system.

-   **Reading Speed:** The reading speed of the access log is currently limited
    by the processing that occurs on each line (by my code). To improve this
    read speed, the time taken to process a single line should accessed and
    compared with the time taken to create a secondary thread to process this
    information. If the threaded process takes less time, then each line read
    should be given to a subprocess for analysis to improve the reading speed.

-   **Logging:** Using Python’s `logging` library to keep local logs of this
    logger as this information might be need later (for historical analysis of
    the data, for finding bugs in the system, etc)

-   **Fault Tolerance:** The current logger system is not fault tolerant. This
    means that if it crashes, all the information before it’s crash will be
    lost. To improve this, the state of the logger should be written
    periodically to the disk/database as well as the last line number of the
    access_log read (if needed).

-   **IP prefix/User based traffic classification:** Use the IP prefix (not IP
    address) to determine the WhoIS information and the ISP and AS (Autonomous
    System). This information can the be used identify the ISPs with highest
    traffic which could help in optimizing the user experience (by using a
    server that has better perform for that specific ISP). This can also be used
    to identify user locations.

-   **Server Errors 5xx triggers:** Alert triggers should be set for the Server
    errors (code *500*s) and use their threshold values to identify server
    overloads, DDOS (denial of service) attacks, etc.

-   **Adaptive Client Traffic Patterns:** Use the average traffic per unit time,
    and train learning classifiers to identify any anomaly in traffic behavior.
    This *adaptive* behavior allows for increasing traffic to the server over a
    period of time with having to change the threshold value again and again.

-   **Historical Analysis:** This logger only tracks the real-time information
    of the access log. A support for going over past log file and looking for
    alerts/triggers should also be added.

-   **Low Traffic Alerts: **This is could indicate either a problem with the
    server (server going down, and hence not writing any logs) or something that
    is preventing the users from reaching the server (network errors).
