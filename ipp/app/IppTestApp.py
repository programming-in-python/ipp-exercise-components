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

import argparse
import logging
import os
import traceback

from time import sleep

import ipp.common.ConfigConst as ConfigConst

from ipp.common.ConfigUtil import ConfigUtil

LOG_FORMAT = "%(asctime)s:::%(thread)d:%(name)s.%(module)s.%(funcName)s()[%(lineno)s]:%(levelname)s:%(message)s"
logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG)

class IppTestApp():
	"""
	Definition of the IppTestApp class.
	
	"""
	
	def __init__(self):
		"""
		Initialization of class.
		
		@param path The name of the resource to apply to the URI.
		"""
		logging.info("Initializing IPP Test App...")

		self.isStarted = False

	def isAppStarted(self) -> bool:
		"""
		"""
		return self.isStarted
	
	def startApp(self):
		"""
		Start the IPP Test App.
		
		"""
		logging.info("Starting Ipp Test App...")
		
		# NOTE: Loading the config file may not be necessary for every use case
		#       If not, the following SLOC's can be commented out and replaced
		#       with alternative logic.
		configUtil = ConfigUtil()

		if (configUtil.isConfigDataLoaded()):
			# TODO: Add other startup logic here

			self.isStarted = True

			logging.info("Ipp Test App started.")
		else:
			logging.error("Failed to load config file and properly initialize app. Ipp Test App not started.")

	def stopApp(self, code: int):
		"""
		Stop the Ipp Test App. Calls stopManager() on the device data manager instance.
		
		"""
		if (self.isStarted):
			logging.info("Ipp Test App stopping...")

			# TODO: Add other shutdown logic here

			logging.info("Ipp Test App stopped with exit code %s.", str(code))
		else:
			logging.info("Ipp Test App not yet started.")

			pass
		
def main():
	"""
	Main function definition for running client as application.
	
	Current implementation runs for 65 seconds then exits.
	"""
	argParser = argparse.ArgumentParser( \
		description = 'Ipp Test App for basic test functions and data set simulation as part of the Intro to Python Programming course.')
	
	argParser.add_argument('-c', '--configFile', help = 'Optional custom configuration file for the Ipp Test App.')

	configFile = None

	try:
		args = argParser.parse_args()
		configFile = args.configFile

		logging.info('Parsed configuration file arg: %s', configFile)
	except:
		logging.info('No arguments to parse.')

	# init ConfigUtil
	configUtil = ConfigUtil(configFile)
	ita = None

	try:
		# init Ipp Test App
		ita = IppTestApp()

		# start Ipp Test App
		ita.startApp()

		# check if Ipp Test App should run forever
		runForever = configUtil.getBoolean(ConfigConst.IPP_TEST_APP, ConfigConst.RUN_FOREVER_KEY)

		if runForever:
			# sleep ~5 seconds every loop
			while (True):
				sleep(5)
			
		else:
			# run Ipp Test App for ~65 seconds then exit
			if (ita.isAppStarted()):
				sleep(65)
				ita.stopApp(0)
			
	except KeyboardInterrupt:
		logging.warning('Keyboard interruption for Ipp Test App. Exiting.')

		if (ita):
			ita.stopApp(-1)

	except Exception as e:
		# handle any uncaught exception that may be thrown
		# during Ipp Test App initialization
		logging.error('Startup exception caused Ipp Test App to fail. Exiting.')
		traceback.print_exception(type(e), e, e.__traceback__)

		if (ita):
			ita.stopApp(-2)

	# unnecessary
	logging.info('Exiting Ipp Test App.')
	exit()

if __name__ == '__main__':
	"""
	Attribute definition for when invoking as app via command line
	
	"""
	main()
	
def parseArgs(self, args):
	"""
	Parse command line args.
	
	@param args The arguments to parse.
	"""
	logging.info("Parsing command line args...")
