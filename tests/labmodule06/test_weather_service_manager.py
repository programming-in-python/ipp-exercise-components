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
import time
import unittest

try:
    from ipp.exercises.labmodule05.location_data import LocationData  # noqa: F401  (prerequisite availability guard)
    from ipp.exercises.labmodule05.time_and_date_util import TimeAndDateUtil  # noqa: F401  (prerequisite availability guard)
    from ipp.exercises.labmodule05.weather_data import WeatherData  # noqa: F401  (prerequisite availability guard)
    from ipp.exercises.labmodule06.weather_service_manager import WeatherServiceManager

    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule06/weather_service_manager.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class WeatherServiceManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format="%(asctime)s:%(module)s:%(levelname)s:%(message)s",
            level=logging.DEBUG,
        )
        logging.info("Testing WeatherServiceManager class...")

    def setUp(self):
        self.weather_svc_mgr = WeatherServiceManager()

    def tearDown(self):
        pass

    def test_weather_service_manager_execution(self):
        self.weather_svc_mgr.start_manager()

        # run for ~2 minutes
        time.sleep(120)

        self.weather_svc_mgr.stop_manager()

        # TODO: Add other tests if you'd like
