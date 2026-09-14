##
# MIT License
# 
# Copyright (c) 2020 - 2025 Andrew D. King
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

import ipp.common.config_const as config_const

from ipp.common.config_util import ConfigUtil

class ConfigUtilCustomTest(unittest.TestCase):
    """
    This test case class contains very basic unit tests for
    ConfigUtil. It should not be considered complete,
    but serve as a starting point for the student implementing
    additional functionality within their Programming the IoT
    environment.
    """
    DEFAULT_USER = "Foo"
    DEFAULT_AUTH = "Bar"
    
    # optionally test the following files
    #  - EmptyTestConfig.cfg
    #  - InvalidTestConfig.cfg
    #  - None (which will default to ./config/IppConfig.cfg)
    config_file = os.path.dirname(__file__) + "/ValidTestConfig.cfg"
    
    @classmethod
    def setUpClass(self):
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        logging.info("Testing ConfigUtil class (custom file load)...")

        self.config_util = ConfigUtil(config_file = self.config_file)
        
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_get_boolean_property(self):
        enable_logging = self.config_util.has_property(config_const.IPP_TEST_APP, config_const.ENABLE_LOGGING_KEY)
        self.assertTrue(enable_logging)
    
    def test_get_integer_property(self):
        port = self.config_util.get_integer(config_const.MQTT_GATEWAY_SERVICE, config_const.PORT_KEY)
        self.assertEqual(port, config_const.DEFAULT_MQTT_PORT)
    
    def test_get_float_property(self):
        h_sim_floor = self.config_util.get_float(config_const.IPP_TEST_APP, config_const.HUMIDITY_SIM_FLOOR_KEY)
        self.assertGreater(h_sim_floor, 0.0)
    
    def test_get_property(self):
        host_name = self.config_util.get_property(config_const.MQTT_GATEWAY_SERVICE, config_const.HOST_KEY)
        self.assertTrue(host_name)
    
    def test_has_property(self):
        self.assertTrue(self.config_util.has_property(config_const.IPP_TEST_APP, config_const.ENABLE_EMULATOR_KEY))

    def test_has_section(self):
        self.assertTrue(self.config_util.has_section(config_const.IPP_TEST_APP))
    
    def test_is_config_data_loaded(self):
        self.assertTrue(self.config_util.is_config_data_loaded())
    
if __name__ == "__main__":
    unittest.main()
