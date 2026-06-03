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
import os
import unittest
import tempfile

from typing import List

try:
	from ipp.exercises.labmodule07.FileUtil import FileUtil
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "FileUtil not yet implemented")
class FileUtilTest(unittest.TestCase):

	TEST_PATH = tempfile.gettempdir()
	TEST_FILE = "IppTestFile.txt"

	@classmethod
	def setUpClass(self):
		logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
		logging.info("Testing FileUtil class...")
		
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testReadFile(self):
		fileName = self._createTestFileName()
		testData = self._createTestData()

		# write the file first to make sure it exists
		FileUtil.writeTextFile(fileName = fileName, content = testData)

		# load the data
		loadedData = FileUtil.readTextFile(fileName = fileName)

		# check if it matches the data just written
		self.assertEqual(loadedData, testData)
		
		# TODO: Add other tests if you'd like
	
	def testWriteFile(self):
		fileName = self._createTestFileName()
		testData = self._createTestData()

		self.assertTrue(FileUtil.writeTextFile(fileName = fileName, content = testData))

		loadedData = FileUtil.readTextFile(fileName = fileName)

		self.assertEqual(loadedData, testData)
		
		# TODO: Add other tests if you'd like
	
	def testDoesFileExist(self):
		fileName = self._createTestFileName()
		
		# not ideal to call a unit test from another unit test...
		# but for now, good enough as we need to be sure
		# the file is there before we check if the FileUtil.fileExists()
		# actually works
		self.testWriteFile()

		self.assertTrue(FileUtil.fileExists(fileName = fileName))

		# TODO: Add other tests if you'd like
	
	def testDoesPathExist(self):
		dirName = tempfile.gettempdir()

		self.assertTrue(FileUtil.directoryExists(dirName = dirName))

		# TODO: Add other tests if you'd like
	
	def _createTestFileName(self) -> str:
		fileName = os.path.join(tempfile.gettempdir(), FileUtilTest.TEST_FILE)

		# TODO: Add other tests if you'd like
	
		return fileName

	def _createTestData(self) -> str:
		testData = "Test data only. Nothing to see here."
	
		# TODO: Add other tests if you'd like
	
		return testData
	