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

from __future__ import annotations

import logging
import sys
import unittest

try:
    from ipp.exercises.labmodule08.user_input_listener import UserInputListener
    from ipp.exercises.labmodule08.user_input_processor import UserInputProcessor
    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False
    # Fallback base so this module still imports (and skips cleanly) before
    # the solution exists. A base class is evaluated eagerly when the class
    # is defined, so without this the SimpleTestListener helper below would
    # subclass an undefined name and raise NameError at import time rather
    # than skipping. Annotations are deferred by the __future__ import above,
    # so the guarded types used only in hints need no fallback.
    UserInputListener = object

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule08/user_input_processor.py."
)


class SimpleTestListener(UserInputListener):
    """
    Minimal UserInputListener used only for testing.

    Stores every received input string. When the number of received
    inputs reaches stop_after, it calls stop_input_listener() on the
    processor so _process_queue() exits cleanly.
    """

    def __init__(self, processor: UserInputProcessor, stop_after: int = 1):
        """
        Store the processor and the number of inputs to collect.

        Args:
            processor: The ``UserInputProcessor`` to stop when done.
            stop_after: How many inputs to collect before stopping.
        """
        super().__init__()
        self.processor      = processor
        self.stop_after      = stop_after
        self.received_inputs = []

        # TODO: Add other tests if you'd like
    
    def handle_user_input(self, input_data: str = None):
        self.received_inputs.append(input_data)
        logging.info("SimpleTestListener received: [%s]", input_data)

        if len(self.received_inputs) >= self.stop_after:
            self.processor.stop_input_listener()

        # TODO: Add other tests if you'd like
    

# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
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
        self.processor.is_listening = False

    # -----------------------------------------------------------------------
    # parse_input tests
    # -----------------------------------------------------------------------

    def test_parse_input_returns_clean_string(self):
        """
        Normal input should come back trimmed.
        """
        result = self.processor.parse_input(raw_input = "  hello world  ")
        self.assertEqual(result, "hello world")

        # TODO: Add other tests if you'd like
    
    def test_parse_input_handles_leading_whitespace(self):
        result = self.processor.parse_input(raw_input = "   tell me about the weather")
        self.assertEqual(result, "tell me about the weather")

        # TODO: Add other tests if you'd like
    
    def test_parse_input_handles_trailing_whitespace(self):
        result = self.processor.parse_input(raw_input = "what is the temperature?   ")
        self.assertEqual(result, "what is the temperature?")

        # TODO: Add other tests if you'd like
    
    def test_parse_input_returns_empty_string_for_whitespace_only(self):
        result = self.processor.parse_input(raw_input = "     ")
        self.assertEqual(result, "")

        # TODO: Add other tests if you'd like
    
    def test_parse_input_returns_empty_string_for_none(self):
        result = self.processor.parse_input(raw_input = None)
        self.assertEqual(result, "")

        # TODO: Add other tests if you'd like
    
    def test_parse_input_preserves_internal_spaces(self):
        result = self.processor.parse_input(raw_input = "what is the forecast for Boston?")
        self.assertEqual(result, "what is the forecast for Boston?")

        # TODO: Add other tests if you'd like
    
    # -----------------------------------------------------------------------
    # Lifecycle tests
    # -----------------------------------------------------------------------

    def test_start_input_listener_returns_false_with_no_listener(self):
        started = self.processor.start_input_listener(listener = None)
        self.assertFalse(started)

        # TODO: Add other tests if you'd like
    
    def test_is_input_listener_started_after_stop(self):
        self.processor.is_listening = True
        self.processor.stop_input_listener()
        self.assertFalse(self.processor.is_input_listener_started())

        # TODO: Add other tests if you'd like
    
    def test_start_input_listener_returns_false_if_already_running(self):
        self.processor.is_listening = True
        second_start = self.processor.start_input_listener(listener = SimpleTestListener(self.processor))
        self.assertFalse(second_start)

        # TODO: Add other tests if you'd like
    
    # -----------------------------------------------------------------------
    # Queue processing tests — pre-load the queue, drive _process_queue directly
    # -----------------------------------------------------------------------

    def test_listener_receives_parsed_input(self):
        """
        A single queued string should be delivered trimmed to the listener.
        """
        listener = SimpleTestListener(self.processor, stop_after = 1)
        self.processor.input_listener = listener
        self.processor.input_queue.put("  what is the humidity today?  ")

        self.processor.is_listening = True
        self.processor._process_queue()

        self.assertEqual(len(listener.received_inputs), 1)
        self.assertEqual(listener.received_inputs[0], "what is the humidity today?")

        # TODO: Add other tests if you'd like
    
    def test_listener_receives_multiple_inputs(self):
        """
        Multiple queued strings should be delivered in order.
        """
        listener = SimpleTestListener(self.processor, stop_after = 3)
        self.processor.input_listener = listener
        self.processor.input_queue.put("first question")
        self.processor.input_queue.put("  second question  ")
        self.processor.input_queue.put("third question")

        self.processor.is_listening = True
        self.processor._process_queue()

        self.assertEqual(len(listener.received_inputs), 3)
        self.assertEqual(listener.received_inputs[0], "first question")
        self.assertEqual(listener.received_inputs[1], "second question")
        self.assertEqual(listener.received_inputs[2], "third question")

        # TODO: Add other tests if you'd like
    
    def test_listener_ignores_empty_input(self):
        """
        Whitespace-only lines should not be delivered to the listener.
        """
        listener = SimpleTestListener(self.processor, stop_after = 1)
        self.processor.input_listener = listener
        self.processor.input_queue.put("   ")
        self.processor.input_queue.put("")
        # Put a real input last so the listener can stop the processor
        self.processor.input_queue.put("real input")

        self.processor.is_listening = True
        self.processor._process_queue()

        self.assertEqual(len(listener.received_inputs), 1)
        self.assertEqual(listener.received_inputs[0], "real input")

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
    