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
import random
import time
import unittest
from threading import Thread

try:
    from ipp.exercises.labmodule05.location_data import LocationData
    from ipp.exercises.labmodule05.time_and_date_util import TimeAndDateUtil  # noqa: F401  (prerequisite availability guard)
    from ipp.exercises.labmodule05.weather_data import WeatherData
    from ipp.exercises.labmodule05.weather_info_container import WindData
    from ipp.exercises.labmodule06.noaa_weather_service_connector import (
        NoaaWeatherServiceConnector,
    )
    from ipp.exercises.labmodule06.weather_data_listener import WeatherDataListener
    from ipp.exercises.labmodule06.weather_service_connector import (
        WeatherServiceConnector,
    )
    from ipp.exercises.labmodule08.live_weather_data_client_visualizer import (
        LiveWeatherDataClientVisualizer,
    )

    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule08/live_weather_data_client_visualizer.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class LiveWeatherDataClientVisualizerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format="%(asctime)s:%(module)s:%(levelname)s:%(message)s",
            level=logging.DEBUG,
        )
        logging.info("Testing LiveWeatherDataClientVisualizer class...")

    def setUp(self):
        self.weather_data_viz = LiveWeatherDataClientVisualizer()

    def tearDown(self):
        pass

    def test_weather_data_visualizer_with_sim_data(self):
        # Create the visualizer
        visualizer = LiveWeatherDataClientVisualizer()

        # Start data simulation in background
        data_thread = Thread(target=self._simulate_weather_data, daemon=True)
        data_thread.start()

        # Start the web server (blocks until stopped with CTRL+C)
        visualizer.start_visualizer()

    def test_weather_data_visualizer_with_live_data(self):
        # Create the visualizer
        weather_svc = NoaaWeatherServiceConnector()
        visualizer = LiveWeatherDataClientVisualizer()

        self.assertTrue(weather_svc.connect_to_service())
        time.sleep(5)

        # Start data simulation in background
        data_thread = Thread(
            target=self._poll_live_weather_data,
            args=(weather_svc, visualizer),
            daemon=True,
        )
        data_thread.start()

        # Start the web server (blocks until stopped with CTRL+C)
        visualizer.start_visualizer()

        time.sleep(10)

        self.assertTrue(weather_svc.disconnect_from_service())

    def _create_sample_weather_data(self, station: str = "KBOS") -> WeatherData:
        weather = WeatherData()
        weather.location = self._create_irrelevant_location_data()
        weather.location.name_id = station
        weather.temperature = random.uniform(-10, 35)
        weather.humidity = random.uniform(30, 90)
        weather.pressure = random.uniform(98000, 103000)
        weather.wind = WindData()
        weather.wind.speed_kph = random.uniform(0, 50)

    def _create_irrelevant_location_data(self, station: str = "KBOS") -> LocationData:
        loc_data = LocationData()
        loc_data.name = station
        loc_data.city = station
        loc_data.region = station
        loc_data.country = station
        loc_data.latitude = 0.0
        loc_data.longitude = 0.0

        return loc_data

    def _poll_live_weather_data(
        self,
        weather_svc: WeatherServiceConnector = None,
        visualizer: WeatherDataListener = None,
    ):
        time.sleep(3)  # Wait for server to start

        stations = ["KBOS", "KLGA", "KJFK"]

        while True:
            for station in stations:
                logging.info(f"Requesting live weather data for {station}")
                # Get the latest data
                weather_data = weather_svc.get_latest_weather_data()

                # Send to visualizer
                visualizer.handle_incoming_weather_data(weather_data)

            time.sleep(5)  # Update every 5 seconds

    def _simulate_weather_data(self, visualizer: WeatherDataListener = None):
        time.sleep(3)  # Wait for server to start

        stations = ["KBOS", "KLGA", "KJFK"]

        while True:
            for station in stations:
                logging.info(f"Generating simulated weather data for {station}")
                weather_data = self._create_sample_weather_data(station=station)

                # Send to visualizer
                visualizer.handle_incoming_weather_data(weather_data)

            time.sleep(3)  # Update every 3 seconds
