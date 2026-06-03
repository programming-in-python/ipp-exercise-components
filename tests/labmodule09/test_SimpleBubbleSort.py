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

import sys
import unittest

try:
    from ipp.exercises.labmodule09.SimpleBubbleSort import SimpleBubbleSort
    MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "SimpleBubbleSort not yet implemented")
class SimpleBubbleSortTest(unittest.TestCase):
    """
    Unit tests for SimpleBubbleSort implementation.
    """
    
    def setUp(self):
        """
        Set up test fixture - runs before each test method.
        """
        self.sorter = SimpleBubbleSort()
    
    def testEmptyList(self):
        """
        Test sorting an empty list.
        """
        data = []
        expected = []
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testSingleElement(self):
        """
        Test sorting a list with single element.
        """
        data = [42]
        expected = [42]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testAlreadySorted(self):
        """
        Test sorting an already sorted list.
        """
        data = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testReverseSorted(self):
        """
        Test sorting a reverse sorted list.
        """
        data = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testRandomNumbers(self):
        """
        Test sorting random integers.
        """
        data = [64, 34, 25, 12, 22, 11, 90]
        expected = [11, 12, 22, 25, 34, 64, 90]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testNegativeNumbers(self):
        """
        Test sorting with negative numbers.
        """
        data = [3, -1, 4, -5, 2, -3]
        expected = [-5, -3, -1, 2, 3, 4]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testDuplicateValues(self):
        """
        Test sorting with duplicate values.
        """
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
        expected = [1, 1, 2, 3, 4, 5, 5, 6, 9]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testStringSorting(self):
        """
        Test sorting strings alphabetically.
        """
        data = ["Thor", "Alice", "Diana", "Bob", "Charlie"]
        expected = ["Alice", "Bob", "Charlie", "Diana", "Thor"]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testFloatingPointNumbers(self):
        """
        Test sorting floating point numbers.
        """
        data = [3.14, 2.71, 1.41, 2.23, 1.73]
        expected = [1.41, 1.73, 2.23, 2.71, 3.14]
        result = self.sorter.sort(data)
        
        self.assertEqual(result, expected)
    
		# TODO: Add other tests if you'd like
	
    def testOriginalListUnchanged(self):
        """
        Test that the original list is not modified.
        """
        data = [3, 1, 4, 1, 5]
        original = data.copy()
        result = self.sorter.sort(data)
        
        # Original should be unchanged
        self.assertEqual(data, original)
        # Result should be sorted
        self.assertEqual(result, [1, 1, 3, 4, 5])

		# TODO: Add other tests if you'd like	

def main():
    """
    Main function to run tests.
    """
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(SimpleBubbleSortTest)
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity = 2)
    result = runner.run(test_suite)
    
    # Return 0 if all tests passed, 1 otherwise
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    """
    Attribute definition for when invoking as app via command line
    """
    sys.exit(main())
