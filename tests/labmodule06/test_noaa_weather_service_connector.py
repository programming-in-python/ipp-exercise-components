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
    from ipp.exercises.labmodule05.location_data import LocationData
    from ipp.exercises.labmodule05.time_and_date_util import TimeAndDateUtil
    from ipp.exercises.labmodule05.weather_data import WeatherData

    from ipp.exercises.labmodule06.noaa_weather_service_connector import NoaaWeatherServiceConnector
    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule06/noaa_weather_service_connector.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class NoaaWeatherServiceConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing NoaaWeatherServiceConnector class...")
        
    def setUp(self):
        self.weather_svc = NoaaWeatherServiceConnector()

    def tearDown(self):
        pass
    
    def test_weather_service_connection(self):
        self.assertTrue(self.weather_svc.connect_to_service())
        time.sleep(5)

        self.assertTrue(self.weather_svc.disconnect_from_service())
        
    def test_weather_service_request_by_station(self):
        loc_data = self._create_sample_location_data()
        
        self.assertTrue(self.weather_svc.connect_to_service())
        time.sleep(5)

        raw_data = self.weather_svc.request_current_weather_data(station_id = "KBOS", loc_data = loc_data)
        json_data = self.weather_svc.get_latest_weather_data_as_json()
        
        print(json_data)

        self.assertIsNotNone(json_data)
        time.sleep(5)

        self.assertTrue(self.weather_svc.disconnect_from_service())
        
        # TODO: Add other tests if you'd like
    
    def test_weather_service_properties(self):
        self.assertEqual(self.weather_svc.get_service_name(), "NOAA Weather Service")
        self.assertEqual(self.weather_svc.get_poll_rate(), 15)
        self.assertEqual(self.weather_svc.get_request_timeout(), 30)

        # TODO: Add other properties
        # TODO: Add other tests if you'd like
        
    def _create_sample_location_data(self) -> LocationData:
        loc_data = LocationData()
        loc_data.name = "My Location"
        loc_data.city = "Boston"
        loc_data.region = "MA"
        loc_data.country = "USA"
        loc_data.latitude = 42.35843
        loc_data.longitude = -71.05977

        return loc_data
