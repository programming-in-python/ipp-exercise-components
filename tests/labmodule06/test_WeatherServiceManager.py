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

	from ipp.exercises.labmodule06.WeatherServiceManager import WeatherServiceManager
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "LocationData, TimeAndDataUtil, WeatherData, WeatherServiceManager not yet implemented")
class WeatherServiceManagerTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing WeatherServiceManager class...")
		
	def setUp(self):
		self.weatherSvcMgr = WeatherServiceManager()

	def tearDown(self):
		pass
	
	def testWeatherServiceManagerExecution(self):
		self.weatherSvcMgr.startManager()

		# run for ~2 minutes
		time.sleep(120)

		self.weatherSvcMgr.stopManager()
		
		# TODO: Add other tests if you'd like
	
