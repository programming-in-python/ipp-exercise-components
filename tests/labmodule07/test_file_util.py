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
import os
import tempfile
import unittest

try:
    from ipp.exercises.labmodule07.file_util import FileUtil

    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create ipp/exercises/labmodule07/file_util.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class FileUtilTest(unittest.TestCase):
    TEST_PATH = tempfile.gettempdir()
    TEST_FILE = "IppTestFile.txt"

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format="%(asctime)s:%(module)s:%(levelname)s:%(message)s",
            level=logging.DEBUG,
        )
        logging.info("Testing FileUtil class...")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_file(self):
        file_name = self._create_test_file_name()
        test_data = self._create_test_data()

        # write the file first to make sure it exists
        FileUtil.write_text_file(file_name=file_name, content=test_data)

        # load the data
        loaded_data = FileUtil.read_text_file(file_name=file_name)

        # check if it matches the data just written
        self.assertEqual(loaded_data, test_data)

        # TODO: Add other tests if you'd like

    def test_write_file(self):
        file_name = self._create_test_file_name()
        test_data = self._create_test_data()

        self.assertTrue(
            FileUtil.write_text_file(file_name=file_name, content=test_data)
        )

        loaded_data = FileUtil.read_text_file(file_name=file_name)

        self.assertEqual(loaded_data, test_data)

        # TODO: Add other tests if you'd like

    def test_does_file_exist(self):
        file_name = self._create_test_file_name()

        # not ideal to call a unit test from another unit test...
        # but for now, good enough as we need to be sure
        # the file is there before we check if the FileUtil.file_exists()
        # actually works
        self.test_write_file()

        self.assertTrue(FileUtil.file_exists(file_name=file_name))

        # TODO: Add other tests if you'd like

    def test_does_path_exist(self):
        dir_name = tempfile.gettempdir()

        self.assertTrue(FileUtil.directory_exists(dir_name=dir_name))

        # TODO: Add other tests if you'd like

    def _create_test_file_name(self) -> str:
        file_name = os.path.join(tempfile.gettempdir(), FileUtilTest.TEST_FILE)

        # TODO: Add other tests if you'd like

        return file_name

    def _create_test_data(self) -> str:
        test_data = "Test data only. Nothing to see here."

        # TODO: Add other tests if you'd like

        return test_data
