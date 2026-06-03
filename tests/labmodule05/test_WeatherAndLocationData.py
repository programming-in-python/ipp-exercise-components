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

import logging
import unittest

from datetime import datetime

try:
	from ipp.exercises.labmodule05.LocationData import LocationData
	from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
	from ipp.exercises.labmodule05.WeatherData import WeatherData
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "LocationData, TimeAndDataUtil, WeatherData not yet implemented")
class WeatherAndLocationDataTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing WeatherData and LocationData classes...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testWeatherDataContainerDefaultValues(self):
		wData = WeatherData()
		isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
		
		self.assertEqual(wData.source, "")
		self.assertEqual(wData.url, "")
		self.assertEqual(wData.description, "")

		self.assertEqual(wData.temperature, 0.0)
		self.assertEqual(wData.humidity, 0.0)
		self.assertEqual(wData.pressure, 0.0)
		self.assertEqual(wData.windspeed, 0.0)

		timestampA = datetime.fromisoformat(wData.timestamp).timestamp()
		timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
		
		# assert they're within 5 seconds
		self.assertAlmostEqual(timestampA, timestampB, delta = 5.0)
		
		self.assertIsNotNone(wData.location)

		# TODO: add other tests if you'd like

	def testWeatherDataContainerCustomValues(self):
		isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
		locData = LocationData()
		wData = WeatherData()

		wData.source = "test"
		wData.url = "https://www.example.com"
		wData.description = "My weather site."
		wData.timestamp = isoTimeDate
		wData.temperature = 15.0
		wData.humidity = 45.0
		wData.pressure = 1005.0
		wData.windspeed = 5.0
		wData.location = locData

		self.assertEqual(wData.source, "test")
		self.assertEqual(wData.url, "https://www.example.com")
		self.assertEqual(wData.description, "My weather site.")
		self.assertEqual(wData.timestamp, isoTimeDate)

		self.assertEqual(wData.temperature, 15.0)
		self.assertEqual(wData.humidity, 45.0)
		self.assertEqual(wData.pressure, 1005.0)
		self.assertEqual(wData.windspeed, 5.0)

		self.assertEqual(wData.location, locData)
		
		# TODO: add other tests if you'd like

	def testLocationDataContainerDefaultValues(self):
		locData = LocationData()

		self.assertEqual(locData.name, "")
		self.assertEqual(locData.city, "")
		self.assertEqual(locData.region, "")
		self.assertEqual(locData.country, "")

		self.assertEqual(locData.latitude, 0.0)
		self.assertEqual(locData.longitude, 0.0)
		self.assertEqual(locData.elevation, 0.0)

		# TODO: add other tests if you'd like

	def testLocationDataContainerCustomValues(self):
		locData = LocationData()

		locData.name = "My Location"
		locData.city = "Boston"
		locData.region = "MA"
		locData.country = "USA"

		self.assertEqual(locData.name, "My Location")
		self.assertEqual(locData.city, "Boston")
		self.assertEqual(locData.region, "MA")
		self.assertEqual(locData.country, "USA")

		# TODO: add other tests if you'd like
		#       (e.g., for lat, lon, elevation)
