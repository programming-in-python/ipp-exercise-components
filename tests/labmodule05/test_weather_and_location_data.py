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
    from ipp.exercises.labmodule05.location_data import LocationData
    from ipp.exercises.labmodule05.time_and_date_util import TimeAndDateUtil
    from ipp.exercises.labmodule05.weather_data import WeatherData

    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "the labmodule05 data classes under ipp/exercises/labmodule05/."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class WeatherAndLocationDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format="%(asctime)s:%(module)s:%(levelname)s:%(message)s",
            level=logging.DEBUG,
        )
        logging.info("Testing WeatherData and LocationData classes...")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_weather_data_container_default_values(self):
        w_data = WeatherData()
        iso_time_date = TimeAndDateUtil.get_current_iso8601_local_date()

        self.assertEqual(w_data.source, "")
        self.assertEqual(w_data.url, "")
        self.assertEqual(w_data.description, "")

        self.assertEqual(w_data.temperature, 0.0)
        self.assertEqual(w_data.humidity, 0.0)
        self.assertEqual(w_data.pressure, 0.0)
        self.assertEqual(w_data.windspeed, 0.0)

        timestamp_a = datetime.fromisoformat(w_data.timestamp).timestamp()
        timestamp_b = datetime.fromisoformat(iso_time_date).timestamp()

        # assert they're within 5 seconds
        self.assertAlmostEqual(timestamp_a, timestamp_b, delta=5.0)

        self.assertIsNotNone(w_data.location)

        # TODO: add other tests if you'd like

    def test_weather_data_container_custom_values(self):
        iso_time_date = TimeAndDateUtil.get_current_iso8601_local_date()
        loc_data = LocationData()
        w_data = WeatherData()

        w_data.source = "test"
        w_data.url = "https://www.example.com"
        w_data.description = "My weather site."
        w_data.timestamp = iso_time_date
        w_data.temperature = 15.0
        w_data.humidity = 45.0
        w_data.pressure = 1005.0
        w_data.windspeed = 5.0
        w_data.location = loc_data

        self.assertEqual(w_data.source, "test")
        self.assertEqual(w_data.url, "https://www.example.com")
        self.assertEqual(w_data.description, "My weather site.")
        self.assertEqual(w_data.timestamp, iso_time_date)

        self.assertEqual(w_data.temperature, 15.0)
        self.assertEqual(w_data.humidity, 45.0)
        self.assertEqual(w_data.pressure, 1005.0)
        self.assertEqual(w_data.windspeed, 5.0)

        self.assertEqual(w_data.location, loc_data)

        # TODO: add other tests if you'd like

    def test_location_data_container_default_values(self):
        loc_data = LocationData()

        self.assertEqual(loc_data.name, "")
        self.assertEqual(loc_data.city, "")
        self.assertEqual(loc_data.region, "")
        self.assertEqual(loc_data.country, "")

        self.assertEqual(loc_data.latitude, 0.0)
        self.assertEqual(loc_data.longitude, 0.0)
        self.assertEqual(loc_data.elevation, 0.0)

        # TODO: add other tests if you'd like

    def test_location_data_container_custom_values(self):
        loc_data = LocationData()

        loc_data.name = "My Location"
        loc_data.city = "Boston"
        loc_data.region = "MA"
        loc_data.country = "USA"

        self.assertEqual(loc_data.name, "My Location")
        self.assertEqual(loc_data.city, "Boston")
        self.assertEqual(loc_data.region, "MA")
        self.assertEqual(loc_data.country, "USA")

        # TODO: add other tests if you'd like
        #       (e.g., for lat, lon, elevation)
