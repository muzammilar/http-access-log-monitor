# -*- coding: utf-8 -*-
"""
    monitor.stats
    ~~~~~~~~~~~~~~~~

    A class to contain all the statistics and traffic summary of the system.

    :copyright: None.
    :license: None
"""

import threading

import util


class Stats:
    """ A class for storing the min, max, and average of integer values"""

    def __init__(self):
        self.min = float("inf")
        self.max = float("-inf")
        self.num_inst = 0
        self.totl_sum = 0
        self.average = 0

    def update(self, val):
        """Update the min, max, average values of the stats"""

        self.min = min(self.min, val)
        self.max = max(self.max, val)
        self.num_inst += 1
        self.totl_sum += val
        self.average = self.totl_sum * 1.0 / self.num_inst


class TrafficSummary:
    """A class to capture the overall nature of traffic"""

    def __init__(self):

        self._lock_sections = threading.Lock()
        self._lock_total_hits = threading.Lock()
        self.obj_size = Stats()
        self.overall_hits = 0

        self.http_methods = {}
        self.website_sections = {}
        # server code
        self.server_codes = {str(x):0 for x in xrange(1, 6)}
        self._server_code_translation = {"1": "- 1xx Informational Responses",
                                         "2": "- 2xx Successful Responses   ",
                                         "3": "- 3xx Redirections           ",
                                         "4": "- 4xx Client Errors          ",
                                         "5": "- 5xx Server Errors          "}

    def update(self, request_summary):
        """
        Updates the overall summary based on a single entry

        Parameters
        ----------
        request_summary: tuple
            ``(ip, user_identifier, user, timestp, request_method, url,
                http_protocol, http_code, obj_size)`` with each entry as a
                string

        Returns
        -------
        None
        """

        try:
            # check log validity
            ip, user_identifier, user, timestp, request_method, url, \
                http_protocol, http_code, obj_size = request_summary
            obj_size = int(obj_size)

            if http_code[0] not in self.server_codes:
                return

            # website sections
            url_subsec = url.split("/")
            len_url_subsec = len(url_subsec)
            if len_url_subsec < 2:  # invalid uri
                return
            website_section = url.split("/")[1]
            with self._lock_sections:
                if website_section not in self.website_sections:
                    self.website_sections[website_section] = 0
                self.website_sections[website_section] += 1

        except:
            print "Error! Check Summary Stats"
            pass

        # add http method
        if request_method not in self.http_methods:
            self.http_methods[request_method] = 0
        self.http_methods[request_method] += 1

        # overall hits
        with self._lock_total_hits:
            self.overall_hits += 1
        self.obj_size.update(obj_size)

        response_code_prefix = http_code[0]
        self.server_codes[response_code_prefix] += 1

    def _get_section_with_max_hits_periodic(self):
        """ Returns the list of sections with the maximum hits in desc order
        and cleans the section-based stats

        Returns
        --------
        sections_with_count [{section, count}, ...]:
            A ``list`` of ``{section, count}`` tuples in descending order of
            count
        """

        with self._lock_sections:
            #sections = sorted(self.website_sections,
            #                  key=self.website_sections.get, reverse=True)
            #sections_with_count = [(sec, self.website_sections[sec])
            #                       for sec in sections]
            # sort on descending count and ascending alphabetical order
            sections_with_count = [(section, count)
                                   for (section, count) in
                                   sorted(self.website_sections.iteritems(),
                                          key=lambda(sec, cnt): (-cnt, sec))]
            self.website_sections.clear()  # truncate the sections
            return sections_with_count

    def get_total_hits(self):
        with self._lock_total_hits:
            return self.overall_hits

    def print_traffic_summary_periodic(self, alert_history):
        """
        Prints the summary of the system, periodically.

        Parameters
        ----------
        alert_history : <AlertHistory>
            An instance of the ``Class <AlertHistory>`` containing
            all the historical alerts generated/recovered.

        Returns
        -------
        None
        """

        sections_summary = self._get_section_with_max_hits_periodic()

        # added cross-platform support for Windows client.
        util.clear_screen()

        total_traffic_period = 0

        # print summary
        print "*******************************************************"
        print "****              Traffic Monitor             *********"
        print "*******************************************************"

        print "***  10s period  ***"
        print "~~~~~~~~~~~~~~~~~~~~"
        print "*******************************************************"
        print "Top 5 Sections:-"
        for idx, section_info in enumerate(sections_summary):
            if idx < 5:   # print only top 5
                print "- /" + section_info[0] + " :\t", section_info[1]
            total_traffic_period += section_info[1]
        print "Total Requests (in the last 10s): \t", total_traffic_period

        print " "
        print "*******************************************************"
        print "***    Overall    ***"
        print "~~~~~~~~~~~~~~~~~~~~"
        print "*******************************************************"
        print "Total Requests: \t", self.overall_hits

        print " "
        print "Response Summary:-"
        for server_cde_prefix in xrange(1, 6):
            cde = str(server_cde_prefix)
            print self._server_code_translation[cde], " : \t", self.server_codes[cde]

        print " "
        print "Response size (in KBs):-"
        print "- Min                  :\t", self.obj_size.min / 1024.0
        print "- Max                  :\t", self.obj_size.max / 1024.0
        print "- Average (per request):\t", self.obj_size.average / 1024.0
        print "- Total data           :\t", self.obj_size.totl_sum / 1024.0

        print " "
        print "HTTP Request Method Types:-"
        for method in self.http_methods:
            print "- ", method, ":\t", self.http_methods[method]

        print "*******************************************************"
        print " "
        print " "

        # print alerts
        alert_history.print_alerts()

