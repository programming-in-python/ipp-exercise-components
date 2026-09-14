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

import datetime
import logging
import time
import unittest

try:
    from ipp.exercises.labmodule05.time_and_date_util import TimeAndDateUtil
    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule05/time_and_date_util.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class TimeAndDateUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing TimeAndDateUtil class...")
        
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_get_current_local_date_in_millis(self):
        # it will absolutely be greater than 0
        self.assertGreater(TimeAndDateUtil.get_current_local_date_in_millis(), 0)

        # compare with our own retrieved value - they won't be exact,
        # but since these two calls happen in sequence, we can expect
        # that - on most modern systems - they'll be within a few
        # seconds of one another

        cur_seconds_a = TimeAndDateUtil.get_current_local_date_in_millis() / 1000
        cur_seconds_b = time.time()

        # this may fail on REALLY slow systems
        self.assertAlmostEqual(cur_seconds_a, cur_seconds_b, 1)

        # TODO: add other tests if you'd like

    def test_get_current_iso8601_local_date(self):
        cur_iso8601_date_a = TimeAndDateUtil.get_current_iso8601_local_date()
        cur_iso8601_date_b = datetime.datetime.fromtimestamp(time.time()).replace(microsecond = 0).isoformat()

        # this may fail on REALLY slow systems
        self.assertEqual(cur_iso8601_date_a, cur_iso8601_date_b)

        # TODO: add other tests if you'd like

    def test_get_iso8601_date_from_millis(self):
        cur_date_in_secs = time.time()

        cur_iso8601_date_a = TimeAndDateUtil.get_iso8601_date_from_millis(cur_date_in_secs * 1000)
        cur_iso8601_date_b = datetime.datetime.fromtimestamp(cur_date_in_secs).replace(microsecond = 0).isoformat()

        # this may fail on REALLY slow systems
        self.assertEqual(cur_iso8601_date_a, cur_iso8601_date_b)

        # TODO: add other tests if you'd like
