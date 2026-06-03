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
	from ipp.exercises.labmodule05.TimeAndDateUtil import TimeAndDateUtil
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "TimeAndDateUtil not yet implemented")
class TimeAndDateUtilTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing TimeAndDateUtil class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testGetCurrentLocalDateInMillis(self):
		# it will absolutely be greater than 0
		self.assertGreater(TimeAndDateUtil.getCurrentLocalDateInMillis(), 0)

		# compare with our own retrieved value - they won't be exact,
		# but since these two calls happen in sequence, we can expect
		# that - on most modern systems - they'll be within a few
		# seconds of one another

		curSecondsA = TimeAndDateUtil.getCurrentLocalDateInMillis() / 1000
		curSecondsB = time.time()

		# this may fail on REALLY slow systems
		self.assertAlmostEqual(curSecondsA, curSecondsB, 1)

		# TODO: add other tests if you'd like

	def testGetCurrentIso8601LocalDate(self):
		curIso8601DateA = TimeAndDateUtil.getCurrentIso8601LocalDate()
		curIso8601DateB = datetime.datetime.fromtimestamp(time.time()).replace(microsecond = 0).isoformat()

		# this may fail on REALLY slow systems
		self.assertEqual(curIso8601DateA, curIso8601DateB)

		# TODO: add other tests if you'd like

	def testGetIso8601DateFromMillis(self):
		curDateInSecs = time.time()

		curIso8601DateA = TimeAndDateUtil.getIso8601DateFromMillis(curDateInSecs * 1000)
		curIso8601DateB = datetime.datetime.fromtimestamp(curDateInSecs).replace(microsecond = 0).isoformat()

		# this may fail on REALLY slow systems
		self.assertEqual(curIso8601DateA, curIso8601DateB)

		# TODO: add other tests if you'd like
