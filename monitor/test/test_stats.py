# -*- coding: utf-8 -*-
"""
    monitor.test.test_stats
    ~~~~~~~~~~~~~~~~

    A set of tests for monitor.stats.

    :copyright: None.
    :license: None
"""
from monitor.stats import Stats, TrafficSummary


class TestStats:
    """ Tests the Stats class """

    def test_count(self):
        stat = Stats()
        stat.update(12)
        stat.update(-1)
        stat.update(9)
        assert(stat.num_inst == 3)

    def test_sum(self):
        stat = Stats()
        stat.update(12)
        stat.update(-1)
        stat.update(9)
        assert(stat.totl_sum == 20)

    def test_average(self):
        stat = Stats()
        stat.update(12)
        stat.update(-1)
        stat.update(9)
        stat.update(4)
        assert(stat.average == 6)

    def test_min(self):
        stat = Stats()
        stat.update(12)
        stat.update(-1)
        stat.update(9)
        stat.update(4)
        assert(stat.min == -1)

    def test_max(self):
        stat = Stats()
        stat.update(12)
        stat.update(-1)
        stat.update(9)
        stat.update(4)
        assert(stat.max == 12)


class TestTrafficSummary:
    """ Tests the Traffic Summary class """

    def test_top_sections(self):
        """ Tests if the top sections are corrrectly sorted,
        first in descending order on the count and second
        on the alphabetical order of the """
        summary = TrafficSummary()
        sections = {'apple': 2, 'banana': 3, 'almond': 2, 'beetroot': 3,
                    'peach': 4}
        sorted_sections = [('peach', 4), ('banana', 3), ('beetroot', 3),
                           ('almond', 2), ('apple', 2)]
        summary.website_sections = sections
        assert (summary._get_section_with_max_hits_periodic() == sorted_sections)
