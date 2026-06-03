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
import random

from threading import Thread

try:
	from ipp.exercises.labmodule05.LocationData import LocationData
	from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
	from ipp.exercises.labmodule05.WeatherData import WeatherData
	from ipp.exercises.labmodule05.WeatherInfoContainer import WindData

	from ipp.exercises.labmodule06.WeatherDataListener import WeatherDataListener
	from ipp.exercises.labmodule06.WeatherServiceConnector import WeatherServiceConnector
	from ipp.exercises.labmodule06.NoaaWeatherServiceConnector import NoaaWeatherServiceConnector
	from ipp.exercises.labmodule08.LiveWeatherDataClientVisualizer import LiveWeatherDataClientVisualizer
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "Required modules not yet implemented")
class LiveWeatherDataClientVisualizerTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing LiveWeatherDataClientVisualizer class...")
		
	def setUp(self):
		self.weatherDataViz = LiveWeatherDataClientVisualizer()

	def tearDown(self):
		pass
	
	def testWeatherDataVisualizerWithSimData(self):
		# Create the visualizer
		visualizer = LiveWeatherDataClientVisualizer()
		
		# Start data simulation in background
		dataThread = Thread(target = self._simulateWeatherData, daemon = True)
		dataThread.start()
		
		# Start the web server (blocks until stopped with CTRL+C)
		visualizer.startVisualizer()
		
	def testWeatherDataVisualizerWithLiveData(self):
		# Create the visualizer
		weatherSvc = NoaaWeatherServiceConnector()
		visualizer = LiveWeatherDataClientVisualizer()
		
		locData = self._createIrrelevantLocationData()
		
		self.assertTrue(weatherSvc.connectToService())
		time.sleep(5)

		# Start data simulation in background
		dataThread = Thread(
			target = self._pollLiveWeatherData,
			args = (weatherSvc, visualizer),
			daemon = True)
		dataThread.start()
		
		# Start the web server (blocks until stopped with CTRL+C)
		visualizer.startVisualizer()

		time.sleep(10)

		self.assertTrue(weatherSvc.disconnectFromService())
		
	def _createSampleWeatherData(self, station: str = "KBOS") -> WeatherData:
		weather = WeatherData()
		weather.location = self._createIrrelevantLocationData()
		weather.location.nameID = station
		weather.temperature = random.uniform(-10, 35)
		weather.humidity = random.uniform(30, 90)
		weather.pressure = random.uniform(98000, 103000)
		weather.wind = WindData()
		weather.wind.speedKph = random.uniform(0, 50)

	def _createIrrelevantLocationData(self, station: str = "KBOS") -> LocationData:
		locData = LocationData()
		locData.name = station
		locData.city = station
		locData.region = station
		locData.country = station
		locData.latitude = 0.0
		locData.longitude = 0.0

		return locData
	
	def _pollLiveWeatherData(self, weatherSvc: WeatherServiceConnector = None, visualizer: WeatherDataListener = None):
		time.sleep(3)  # Wait for server to start
		
		stations = ['KBOS', 'KLGA', 'KJFK']
		
		while True:
			for station in stations:
				logging.info(f"Requesting live weather data for {station}")
				locData = self._createIrrelevantLocationData(station = station)
				
				# Get the latest data
				weatherData = weatherSvc.getLatestWeatherData()

				# Send to visualizer
				visualizer.handleIncomingWeatherData(weatherData)
			
			time.sleep(5)  # Update every 5 seconds

	def _simulateWeatherData(self, visualizer: WeatherDataListener = None):
		time.sleep(3)  # Wait for server to start
		
		stations = ['KBOS', 'KLGA', 'KJFK']
		
		while True:
			for station in stations:
				logging.info(f"Generating simulated weather data for {station}")
				weatherData = self._createSampleWeatherData(station = station)
				
				# Send to visualizer
				visualizer.handleIncomingWeatherData(weatherData)
			
			time.sleep(3)  # Update every 3 seconds
