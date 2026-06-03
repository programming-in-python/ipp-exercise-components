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
import sys
import unittest

try:
	from ipp.exercises.labmodule08.UserInputListener import UserInputListener
	from ipp.exercises.labmodule08.UserInputProcessor import UserInputProcessor
	MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "UserInputListener, UserInputProcessor not yet implemented")
class SimpleTestListener(UserInputListener):
	"""
	Minimal UserInputListener used only for testing.

	Stores every received input string. When the number of received
	inputs reaches stopAfter, it calls stopInputListener() on the
	processor so _processQueue() exits cleanly.
	"""

	def __init__(self, processor: UserInputProcessor, stopAfter: int = 1):
		"""
		@param processor:  The UserInputProcessor to stop when done.
		@param stopAfter:  How many inputs to collect before stopping.
		"""
		super().__init__()
		self.processor      = processor
		self.stopAfter      = stopAfter
		self.receivedInputs = []

		# TODO: Add other tests if you'd like
	
	def handleUserInput(self, inputData: str = None):
		self.receivedInputs.append(inputData)
		logging.info("SimpleTestListener received: [%s]", inputData)

		if len(self.receivedInputs) >= self.stopAfter:
			self.processor.stopInputListener()

		# TODO: Add other tests if you'd like
	

# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class UserInputProcessorTest(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		logging.basicConfig(
			format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s',
			level  = logging.DEBUG
		)
		logging.info("Testing UserInputProcessor and UserInputListener classes...")

	def setUp(self):
		self.processor = UserInputProcessor()

	def tearDown(self):
		self.processor.isListening = False

	# -----------------------------------------------------------------------
	# parseInput tests
	# -----------------------------------------------------------------------

	def testParseInputReturnsCleanString(self):
		"""Normal input should come back trimmed."""
		result = self.processor.parseInput(rawInput = "  hello world  ")
		self.assertEqual(result, "hello world")

		# TODO: Add other tests if you'd like
	
	def testParseInputHandlesLeadingWhitespace(self):
		result = self.processor.parseInput(rawInput = "   tell me about the weather")
		self.assertEqual(result, "tell me about the weather")

		# TODO: Add other tests if you'd like
	
	def testParseInputHandlesTrailingWhitespace(self):
		result = self.processor.parseInput(rawInput = "what is the temperature?   ")
		self.assertEqual(result, "what is the temperature?")

		# TODO: Add other tests if you'd like
	
	def testParseInputReturnsEmptyStringForWhitespaceOnly(self):
		result = self.processor.parseInput(rawInput = "     ")
		self.assertEqual(result, "")

		# TODO: Add other tests if you'd like
	
	def testParseInputReturnsEmptyStringForNone(self):
		result = self.processor.parseInput(rawInput = None)
		self.assertEqual(result, "")

		# TODO: Add other tests if you'd like
	
	def testParseInputPreservesInternalSpaces(self):
		result = self.processor.parseInput(rawInput = "what is the forecast for Boston?")
		self.assertEqual(result, "what is the forecast for Boston?")

		# TODO: Add other tests if you'd like
	
	# -----------------------------------------------------------------------
	# Lifecycle tests
	# -----------------------------------------------------------------------

	def testStartInputListenerReturnsFalseWithNoListener(self):
		started = self.processor.startInputListener(listener = None)
		self.assertFalse(started)

		# TODO: Add other tests if you'd like
	
	def testIsInputListenerStartedAfterStop(self):
		self.processor.isListening = True
		self.processor.stopInputListener()
		self.assertFalse(self.processor.isInputListenerStarted())

		# TODO: Add other tests if you'd like
	
	def testStartInputListenerReturnsFalseIfAlreadyRunning(self):
		self.processor.isListening = True
		second_start = self.processor.startInputListener(listener = SimpleTestListener(self.processor))
		self.assertFalse(second_start)

		# TODO: Add other tests if you'd like
	
	# -----------------------------------------------------------------------
	# Queue processing tests — pre-load the queue, drive _processQueue directly
	# -----------------------------------------------------------------------

	def testListenerReceivesParsedInput(self):
		"""A single queued string should be delivered trimmed to the listener."""
		listener = SimpleTestListener(self.processor, stopAfter = 1)
		self.processor.inputListener = listener
		self.processor.inputQueue.put("  what is the humidity today?  ")

		self.processor.isListening = True
		self.processor._processQueue()

		self.assertEqual(len(listener.receivedInputs), 1)
		self.assertEqual(listener.receivedInputs[0], "what is the humidity today?")

		# TODO: Add other tests if you'd like
	
	def testListenerReceivesMultipleInputs(self):
		"""Multiple queued strings should be delivered in order."""
		listener = SimpleTestListener(self.processor, stopAfter = 3)
		self.processor.inputListener = listener
		self.processor.inputQueue.put("first question")
		self.processor.inputQueue.put("  second question  ")
		self.processor.inputQueue.put("third question")

		self.processor.isListening = True
		self.processor._processQueue()

		self.assertEqual(len(listener.receivedInputs), 3)
		self.assertEqual(listener.receivedInputs[0], "first question")
		self.assertEqual(listener.receivedInputs[1], "second question")
		self.assertEqual(listener.receivedInputs[2], "third question")

		# TODO: Add other tests if you'd like
	
	def testListenerIgnoresEmptyInput(self):
		"""Whitespace-only lines should not be delivered to the listener."""
		listener = SimpleTestListener(self.processor, stopAfter = 1)
		self.processor.inputListener = listener
		self.processor.inputQueue.put("   ")
		self.processor.inputQueue.put("")
		# Put a real input last so the listener can stop the processor
		self.processor.inputQueue.put("real input")

		self.processor.isListening = True
		self.processor._processQueue()

		self.assertEqual(len(listener.receivedInputs), 1)
		self.assertEqual(listener.receivedInputs[0], "real input")

		# TODO: Add other tests if you'd like
	

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
	suite  = unittest.TestLoader().loadTestsFromTestCase(UserInputProcessorTest)
	runner = unittest.TextTestRunner(verbosity = 2)
	result = runner.run(suite)
	return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
	sys.exit(main())
	