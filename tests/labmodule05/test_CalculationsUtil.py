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

try:
	from ipp.exercises.labmodule05.CalculationsUtil import CalculationsUtil
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "CalculationsUtil not yet implemented")
class CalculationsUtilTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing CalculationsUtil class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testDivideTwoIntegers(self):
		self.assertEqual(0.0, CalculationsUtil.divideTwoNumbers(1, 0))
		self.assertEqual(5.0, CalculationsUtil.divideTwoNumbers(10, 2))
		self.assertEqual(2.0, CalculationsUtil.divideTwoNumbers(10, 5))
		self.assertEqual(1.0, CalculationsUtil.divideTwoNumbers(10, 10))

		# TODO: Add other tests if you'd like
	
	def testDivideTwoFloats(self):
		self.assertEqual(0.0, CalculationsUtil.divideTwoNumbers(1.5, 0))
		self.assertEqual(5.5, CalculationsUtil.divideTwoNumbers(11, 2))
		self.assertEqual(2.5, CalculationsUtil.divideTwoNumbers(5, 2))
		self.assertEqual(1.5, CalculationsUtil.divideTwoNumbers(1.5, 1.0))

		# TODO: Add other tests if you'd like
	
	def testFarenheitToCelsiusConversion(self):
		# TODO: Put your test implementation here

		pass

	def testCelsiusToFarenheitConversion(self):
		# TODO: Put your test implementation here
		
		pass
