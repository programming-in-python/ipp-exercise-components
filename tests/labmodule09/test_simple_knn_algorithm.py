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

import unittest

try:
    from ipp.exercises.labmodule09.simple_knn_algorithm import SimpleKnnAlgorithm

    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule09/simple_knn_algorithm.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class SimpleKnnAlgorithmTest(unittest.TestCase):
    """
    Simple set of tests for the SimpleKnnAlgorithm class.
    """

    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.knn = SimpleKnnAlgorithm(k=3)

        # Sample training data: (features, target)
        self.regression_data = [
            ([1.0, 2.0], 10.0),
            ([2.0, 3.0], 15.0),
            ([3.0, 4.0], 20.0),
            ([4.0, 5.0], 25.0),
            ([5.0, 6.0], 30.0),
        ]

        # Classification data (using integer classes)
        self.classification_data = [
            ([1.0, 1.0], 0),
            ([1.5, 1.5], 0),
            ([2.0, 2.0], 0),
            ([8.0, 8.0], 1),
            ([8.5, 8.5], 1),
            ([9.0, 9.0], 1),
        ]

    def test_distance_calculations(self):
        """
        Test both Euclidean and Manhattan distance calculations.
        """
        point1 = [0.0, 0.0]
        point2 = [3.0, 4.0]

        # Test Euclidean distance: sqrt(3^2 + 4^2) = 5.0
        euclidean = self.knn.calculate_euclidean_distance(point1, point2)
        self.assertAlmostEqual(euclidean, 5.0, places=5)

        # Test Manhattan distance: |3| + |4| = 7.0
        manhattan = self.knn.calculate_manhattan_distance(point1, point2)
        self.assertAlmostEqual(manhattan, 7.0, places=5)

        # Test with identical points
        same_point = [1.0, 2.0]
        self.assertAlmostEqual(
            self.knn.calculate_euclidean_distance(same_point, same_point), 0.0, places=5
        )

        # Test with mismatched dimensions
        point3 = [1.0, 2.0, 3.0]
        distance = self.knn.calculate_euclidean_distance(point1, point3)
        self.assertEqual(distance, float("inf"))

        # TODO: Add other tests if you'd like

    def test_training_data_management(self):
        """
        Test setting and validating training data.
        """
        # Test setting valid training data
        self.knn.set_training_data(self.regression_data)
        self.assertEqual(len(self.knn.training_data), 5)
        self.assertEqual(self.knn.training_data, self.regression_data)

        # Test with empty data
        empty_knn = SimpleKnnAlgorithm(k=3)
        empty_knn.set_training_data([])
        self.assertEqual(len(empty_knn.training_data), 0)

        # Test with None
        none_knn = SimpleKnnAlgorithm(k=3)
        none_knn.set_training_data(None)
        self.assertEqual(len(none_knn.training_data), 0)

        # TODO: Add other tests if you'd like

    def test_find_k_nearest(self):
        """
        Test finding k nearest neighbors with both distance metrics.
        """
        self.knn.set_training_data(self.regression_data)
        test_point = [2.5, 3.5]

        # Test with Euclidean distance
        neighbors_euclidean = self.knn.find_k_nearest(test_point, use_euclidean=True)
        self.assertEqual(len(neighbors_euclidean), 3)

        # Verify neighbors are sorted by distance
        for i in range(len(neighbors_euclidean) - 1):
            self.assertLessEqual(
                neighbors_euclidean[i][0], neighbors_euclidean[i + 1][0]
            )

        # Test with Manhattan distance
        neighbors_manhattan = self.knn.find_k_nearest(test_point, use_euclidean=False)
        self.assertEqual(len(neighbors_manhattan), 3)

        # Test with no training data
        empty_knn = SimpleKnnAlgorithm(k=3)
        neighbors_empty = empty_knn.find_k_nearest(test_point)
        self.assertEqual(neighbors_empty, [])

        # TODO: Add other tests if you'd like

    def test_regression_prediction(self):
        """
        Test regression prediction functionality.
        """
        self.knn.set_training_data(self.regression_data)

        # Test prediction on a point between training points
        test_point = [2.5, 3.5]
        prediction = self.knn.predict_regression(test_point)
        self.assertIsInstance(prediction, float)
        self.assertGreater(prediction, 10.0)
        self.assertLess(prediction, 25.0)

        # Test on exact training point
        exact_point = [3.0, 4.0]
        exact_prediction = self.knn.predict_regression(exact_point)
        self.assertAlmostEqual(exact_prediction, 20.0, delta=2.0)

        # Test with no training data
        empty_knn = SimpleKnnAlgorithm(k=3)
        empty_prediction = empty_knn.predict_regression(test_point)
        self.assertIsNone(empty_prediction)

        # Test with Manhattan distance
        manhattan_prediction = self.knn.predict_regression(
            test_point, use_euclidean=False
        )
        self.assertIsNotNone(manhattan_prediction)

        # TODO: Add other tests if you'd like

    def test_classification_prediction(self):
        """
        Test classification prediction functionality.
        """
        self.knn.set_training_data(self.classification_data)

        # Test point close to class 0
        test_point_class0 = [1.2, 1.2]
        prediction0 = self.knn.predict_classification(test_point_class0)
        self.assertEqual(prediction0, 0)

        # Test point close to class 1
        test_point_class1 = [8.2, 8.2]
        prediction1 = self.knn.predict_classification(test_point_class1)
        self.assertEqual(prediction1, 1)

        # Test with no training data
        empty_knn = SimpleKnnAlgorithm(k=3)
        empty_prediction = empty_knn.predict_classification([1.0, 1.0])
        self.assertIsNone(empty_prediction)

        # Test with Manhattan distance
        manhattan_prediction = self.knn.predict_classification(
            test_point_class0, use_euclidean=False
        )
        self.assertIn(manhattan_prediction, [0, 1])

        # TODO: Add other tests if you'd like

    def test_prediction_evaluation(self):
        """
        Test prediction evaluation metrics.
        """
        # Test perfect prediction
        metrics_perfect = self.knn.evaluate_prediction(10.0, 10.0)
        self.assertEqual(metrics_perfect["error"], 0.0)
        self.assertEqual(metrics_perfect["absolute_error"], 0.0)
        self.assertEqual(metrics_perfect["squared_error"], 0.0)
        self.assertEqual(metrics_perfect["percent_error"], 0.0)

        # Test under-prediction
        metrics_under = self.knn.evaluate_prediction(10.0, 8.0)
        self.assertEqual(metrics_under["error"], 2.0)
        self.assertEqual(metrics_under["absolute_error"], 2.0)
        self.assertEqual(metrics_under["squared_error"], 4.0)
        self.assertAlmostEqual(metrics_under["percent_error"], 20.0, places=1)

        # Test over-prediction
        metrics_over = self.knn.evaluate_prediction(10.0, 12.0)
        self.assertEqual(metrics_over["error"], -2.0)
        self.assertEqual(metrics_over["absolute_error"], 2.0)

        # Test with zero actual value and non-zero prediction
        metrics_zero = self.knn.evaluate_prediction(0.0, 5.0)
        self.assertEqual(metrics_zero["percent_error"], float("inf"))

        # Test with both zero
        metrics_both_zero = self.knn.evaluate_prediction(0.0, 0.0)
        self.assertEqual(metrics_both_zero["percent_error"], 0.0)

        # TODO: Add other tests if you'd like


if __name__ == "__main__":
    unittest.main()
