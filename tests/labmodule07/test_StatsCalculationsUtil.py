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

from typing import List

try:
	from ipp.exercises.labmodule07.StatsCalculationsUtil import StatsCalculationsUtil
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "StatsCalculationsUtil not yet implemented")
class StatsCalculationsUtilTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing StatsCalculationsUtil class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testStatsCalculationsUsingStatsData(self):
		values = self._createTestDataList()

		# make sure the derived functionality works

		self.assertEqual(StatsCalculationsUtil.divideTwoNumbers(10, 5), 2)
		self.assertEqual(StatsCalculationsUtil.divideTwoNumbers(5, 0), 0)

		# now test the stats calc
				
		sData = StatsCalculationsUtil.calculateStats(values)
		
		# NOTE: if the test data list values change, these
		# values will need to be updated
		self.assertEqual(sData.count, 10)
		self.assertEqual(sData.mean, 50.0)
		self.assertEqual(sData.median, 50.0)
		self.assertEqual(sData.min, 5.0)
		self.assertEqual(sData.max, 95.0)
		self.assertEqual(round(sData.standardDeviation, 0), 30.0)

		# TODO: Add other tests if you'd like
	
	def _createTestDataList(self) -> List:
		values = []

		values.append(5.0)
		values.append(15.0)
		values.append(25.0)
		values.append(35.0)
		values.append(45.0)
		values.append(55.0)
		values.append(65.0)
		values.append(75.0)
		values.append(85.0)
		values.append(95.0)
	
		return values
	