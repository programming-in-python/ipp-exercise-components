##
# MIT License
# 
# Copyright (c) 2025 Andrew D. King
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import annotations

import logging
import unittest

from datetime import datetime

try:
    from ipp.exercises.labmodule05.time_and_date_util import TimeAndDateUtil
    from ipp.exercises.labmodule07.stats_data import StatsData
    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule07/stats_data.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class StatsDataTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing StatsData class...")
        
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_stats_data_container_default_values(self):
        s_data = StatsData()
        iso_time_date = TimeAndDateUtil.get_current_iso8601_local_date()
        
        self.assertEqual(s_data.count, 0)
        self.assertEqual(s_data.mean, 0.0)
        self.assertEqual(s_data.median, 0.0)
        self.assertEqual(s_data.min, 0.0)
        self.assertEqual(s_data.max, 0.0)
        self.assertEqual(s_data.standard_deviation, 0.0)

        timestamp_a = datetime.fromisoformat(s_data.timestamp).timestamp()
        timestamp_b = datetime.fromisoformat(iso_time_date).timestamp()
        
        # assert they're within 5 seconds
        self.assertAlmostEqual(timestamp_a, timestamp_b, delta = 5.0)
        
        # TODO: Add other tests if you'd like
    
    def test_stats_data_container_custom_values(self):
        s_data = StatsData()
        iso_time_date = TimeAndDateUtil.get_current_iso8601_local_date()
        
        s_data.count = 5
        s_data.mean = 55.0
        s_data.median = 52.0
        s_data.min = 25.0
        s_data.max = 75.0
        s_data.standard_deviation = 2.5

        self.assertEqual(s_data.count, 5)
        self.assertEqual(s_data.mean, 55.0)
        self.assertEqual(s_data.median, 52.0)
        self.assertEqual(s_data.min, 25.0)
        self.assertEqual(s_data.max, 75.0)
        self.assertEqual(s_data.standard_deviation, 2.5)

        timestamp_a = datetime.fromisoformat(s_data.timestamp).timestamp()
        timestamp_b = datetime.fromisoformat(iso_time_date).timestamp()
        
        # assert they're within 5 seconds
        self.assertAlmostEqual(timestamp_a, timestamp_b, delta = 5.0)

        # TODO: Add other tests if you'd like
    