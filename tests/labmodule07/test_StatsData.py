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
	from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
	from ipp.exercises.labmodule07.StatsData import StatsData
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "TimeAndDateUtil, StatsData not yet implemented")
class StatsDataTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing StatsData class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testStatsDataContainerDefaultValues(self):
		sData = StatsData()
		isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
		
		self.assertEqual(sData.count, 0)
		self.assertEqual(sData.mean, 0.0)
		self.assertEqual(sData.median, 0.0)
		self.assertEqual(sData.min, 0.0)
		self.assertEqual(sData.max, 0.0)
		self.assertEqual(sData.standardDeviation, 0.0)

		timestampA = datetime.fromisoformat(sData.timestamp).timestamp()
		timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
		
		# assert they're within 5 seconds
		self.assertAlmostEqual(timestampA, timestampB, delta = 5.0)
		
		# TODO: Add other tests if you'd like
	
	def testStatsDataContainerCustomValues(self):
		sData = StatsData()
		isoTimeDate = TimeAndDateUtil.getCurrentIso8601LocalDate()
		
		sData.count = 5
		sData.mean = 55.0
		sData.median = 52.0
		sData.min = 25.0
		sData.max = 75.0
		sData.standardDeviation = 2.5

		self.assertEqual(sData.count, 5)
		self.assertEqual(sData.mean, 55.0)
		self.assertEqual(sData.median, 52.0)
		self.assertEqual(sData.min, 25.0)
		self.assertEqual(sData.max, 75.0)
		self.assertEqual(sData.standardDeviation, 2.5)

		timestampA = datetime.fromisoformat(sData.timestamp).timestamp()
		timestampB = datetime.fromisoformat(isoTimeDate).timestamp()
		
		# assert they're within 5 seconds
		self.assertAlmostEqual(timestampA, timestampB, delta = 5.0)

		# TODO: Add other tests if you'd like
	