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

import datetime
import logging
import time
import unittest

try:
	from ipp.exercises.labmodule05.LocationData import LocationData
	from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
	from ipp.exercises.labmodule05.WeatherData import WeatherData

	from ipp.exercises.labmodule06.NoaaWeatherServiceConnector import NoaaWeatherServiceConnector
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "LocationData, TimeAndDataUtil, WeatherData, NoaaWeatherServiceConnector not yet implemented")
class NoaaWeatherServiceConnectorTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing NoaaWeatherServiceConnector class...")
		
	def setUp(self):
		self.weatherSvc = NoaaWeatherServiceConnector()

	def tearDown(self):
		pass
	
	def testWeatherServiceConnection(self):
		self.assertTrue(self.weatherSvc.connectToService())
		time.sleep(5)

		self.assertTrue(self.weatherSvc.disconnectFromService())
		
	def testWeatherServiceRequestByStation(self):
		locData = self._createSampleLocationData()
		
		self.assertTrue(self.weatherSvc.connectToService())
		time.sleep(5)

		rawData = self.weatherSvc.requestCurrentWeatherData(stationID = "KBOS", locData = locData)
		jsonData = self.weatherSvc.getLatestWeatherDataAsJson()
		
		print(jsonData)

		self.assertIsNotNone(jsonData)
		time.sleep(5)

		self.assertTrue(self.weatherSvc.disconnectFromService())
		
		# TODO: Add other tests if you'd like
	
	def testWeatherServiceProperties(self):
		self.assertEqual(self.weatherSvc.getServiceName(), "NOAA Weather Service")
		self.assertEqual(self.weatherSvc.getPollRate(), 15)
		self.assertEqual(self.weatherSvc.getRequestTimeout(), 30)

		# TODO: Add other properties
		# TODO: Add other tests if you'd like
		
	def _createSampleLocationData(self) -> LocationData:
		locData = LocationData()
		locData.name = "My Location"
		locData.city = "Boston"
		locData.region = "MA"
		locData.country = "USA"
		locData.latitude = 42.35843
		locData.longitude = -71.05977

		return locData
