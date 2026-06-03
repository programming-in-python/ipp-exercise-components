import unittest
import numpy as np

try:
    from ipp.exercises.labmodule09.SimpleKnnAlgorithm import SimpleKnnAlgorithm
    MODULE_AVAILABLE = True
except ImportError:
	MODULE_AVAILABLE = False

@unittest.skipUnless(MODULE_AVAILABLE, "SimpleKnnAlgorithm not yet implemented")
class KnnAlgorithmTest(unittest.TestCase):
    """
    Unit tests for the KnnAlgorithm class.
    
    This test class comprehensively verifies the functionality of the KNN algorithm
    implementation across multiple values of k for both classification and regression tasks.
    Tests cover edge cases, error conditions, and different parameter combinations.
    """
    
    def setUp(self):
        """Set up test data for classification and regression tests."""
        # Classification test data - binary classification problem
        self.X_train_class = np.array([
            [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],  # Class 0 region
            [1, 1], [2, 2], [3, 3], [4, 4], [5, 5],  # Mixed regions
            [6, 7], [7, 8], [8, 9], [9, 10]          # Class 1 region
        ])
        self.y_train_class = np.array([0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1])
        
        # Regression test data - linear relationship y = 2x
        self.X_train_reg = np.array([
            [1], [2], [3], [4], [5], [6], [7], [8], [9], [10]
        ])
        self.y_train_reg = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
        
        # Test points
        self.X_test_class = np.array([[2.5, 2.5], [4.5, 4.5], [7.5, 7.5]])
        self.X_test_reg = np.array([[2.5], [7.5], [5.0]])
        
        # K values to test (multiple non-zero integers as requested)
        self.k_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
		# TODO: Add other tests if you'd like
	
    def test_initialization(self):
        """Test proper initialization of KnnAlgorithm."""
        knn = SimpleKnnAlgorithm(k=3)
        self.assertEqual(knn.k, 3)
        self.assertEqual(knn.distance_metric, 'euclidean')
        self.assertFalse(knn.is_fitted)
        
        # Test with different distance metric
        knn_manhattan = SimpleKnnAlgorithm(k=5, distance_metric='manhattan')
        self.assertEqual(knn_manhattan.k, 5)
        self.assertEqual(knn_manhattan.distance_metric, 'manhattan')
    
		# TODO: Add other tests if you'd like
	
    def test_invalid_k_initialization(self):
        """Test that invalid k values raise ValueError."""
        with self.assertRaises(ValueError) as context:
            SimpleKnnAlgorithm(k=0)
        self.assertIn("k must be a positive integer", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            SimpleKnnAlgorithm(k=-1)
        self.assertIn("k must be a positive integer", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            SimpleKnnAlgorithm(k=-10)
        self.assertIn("k must be a positive integer", str(context.exception))
    
		# TODO: Add other tests if you'd like
	
    def test_fit_method(self):
        """Test the fit method properly stores training data."""
        knn = SimpleKnnAlgorithm(k=3)
        knn.fit(self.X_train_class, self.y_train_class)
        
        self.assertTrue(knn.is_fitted)
        np.testing.assert_array_equal(knn.X_train, self.X_train_class)
        np.testing.assert_array_equal(knn.y_train, self.y_train_class)
    
		# TODO: Add other tests if you'd like
	
    def test_classification_across_k_values(self):
        """Test classification functionality across multiple k values."""
        for k in self.k_values:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(self.X_train_class, self.y_train_class)
                
                predictions = knn.predict_classification(self.X_test_class)
                
                # Verify predictions are valid class labels
                unique_classes = np.unique(self.y_train_class)
                for pred in predictions:
                    self.assertIn(pred, unique_classes)
                
                # Verify correct number of predictions
                self.assertEqual(len(predictions), len(self.X_test_class))
                
                # Verify predictions are numpy array
                self.assertIsInstance(predictions, np.ndarray)
    
		# TODO: Add other tests if you'd like
	
    def test_regression_across_k_values(self):
        """Test regression functionality across multiple k values."""
        for k in self.k_values:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(self.X_train_reg, self.y_train_reg)
                
                regression_predictor = knn.get_regression_predictor()
                predictions = regression_predictor.predict(self.X_test_reg)
                
                # Verify predictions are reasonable for linear relationship y = 2x
                expected_values = [5.0, 15.0, 10.0]  # 2.5*2, 7.5*2, 5.0*2
                for i, (pred, expected) in enumerate(zip(predictions, expected_values)):
                    self.assertAlmostEqual(pred, expected, delta=3.0, 
                                         msg=f"Prediction {i} with k={k} not close to expected value")
                
                # Verify correct number of predictions
                self.assertEqual(len(predictions), len(self.X_test_reg))
                
                # Verify predictions are numeric
                self.assertTrue(all(isinstance(p, (int, float, np.number)) for p in predictions))
    
		# TODO: Add other tests if you'd like
	
    def test_k_effect_on_predictions(self):
        """Test that different k values can produce different predictions."""
        predictions_by_k = {}
        
        for k in [1, 3, 5]:
            knn = SimpleKnnAlgorithm(k=k)
            knn.fit(self.X_train_class, self.y_train_class)
            predictions = knn.predict_classification(self.X_test_class)
            predictions_by_k[k] = predictions
        
        # At least some k values should produce different predictions
        all_same = all(np.array_equal(predictions_by_k[1], predictions_by_k[k]) 
                      for k in [3, 5])
        self.assertFalse(all_same, "All k values produced identical predictions")
    
		# TODO: Add other tests if you'd like
	
    def test_general_predict_method(self):
        """Test the general predict method for both classification and regression."""
        # Test classification
        knn_class = SimpleKnnAlgorithm(k=3)
        knn_class.fit(self.X_train_class, self.y_train_class)
        
        class_predictions = knn_class.predict(self.X_test_class, task_type='classification')
        direct_predictions = knn_class.predict_classification(self.X_test_class)
        np.testing.assert_array_equal(class_predictions, direct_predictions)
        
        # Test regression
        knn_reg = SimpleKnnAlgorithm(k=3)
        knn_reg.fit(self.X_train_reg, self.y_train_reg)
        
        reg_predictions = knn_reg.predict(self.X_test_reg, task_type='regression')
        self.assertEqual(len(reg_predictions), len(self.X_test_reg))
        
        # Test invalid task type
        with self.assertRaises(ValueError) as context:
            knn_class.predict(self.X_test_class, task_type='invalid')
        self.assertIn("Unsupported task type", str(context.exception))
    
		# TODO: Add other tests if you'd like
	
    def test_distance_metrics(self):
        """Test different distance metrics."""
        for metric in ['euclidean', 'manhattan']:
            with self.subTest(metric=metric):
                knn = SimpleKnnAlgorithm(k=3, distance_metric=metric)
                knn.fit(self.X_train_class, self.y_train_class)
                
                predictions = knn.predict_classification(self.X_test_class)
                self.assertEqual(len(predictions), len(self.X_test_class))
        
        # Test invalid distance metric
        with self.assertRaises(ValueError) as context:
            knn = SimpleKnnAlgorithm(k=3, distance_metric='invalid')
            knn.fit(self.X_train_class, self.y_train_class)
            knn.predict_classification(self.X_test_class)
        self.assertIn("Unsupported distance metric", str(context.exception))
    
		# TODO: Add other tests if you'd like
	
    def test_single_point_prediction(self):
        """Test prediction with a single test point."""
        for k in [1, 3, 5]:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(self.X_train_class, self.y_train_class)
                
                single_point = np.array([2.5, 2.5])
                prediction = knn.predict_classification(single_point)
                
                self.assertEqual(len(prediction), 1)
                self.assertIn(prediction[0], np.unique(self.y_train_class))
    
		# TODO: Add other tests if you'd like
	
    def test_regression_aggregation_methods(self):
        """Test different aggregation methods for regression."""
        for k in [1, 3, 5]:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(self.X_train_reg, self.y_train_reg)
                
                regression_predictor = knn.get_regression_predictor()
                
                for method in ['mean', 'median', 'weighted_mean']:
                    with self.subTest(method=method):
                        predictions = regression_predictor.predict(self.X_test_reg, 
                                                                 aggregation_method=method)
                        self.assertEqual(len(predictions), len(self.X_test_reg))
                        self.assertTrue(all(isinstance(p, (int, float, np.number)) 
                                          for p in predictions))
                
                # Test invalid aggregation method
                with self.assertRaises(ValueError) as context:
                    regression_predictor.predict(self.X_test_reg, aggregation_method='invalid')
                self.assertIn("Unsupported aggregation method", str(context.exception))
    
		# TODO: Add other tests if you'd like
	
    def test_unfitted_model_error(self):
        """Test that using an unfitted model raises an error."""
        knn = SimpleKnnAlgorithm(k=3)
        
        with self.assertRaises(ValueError) as context:
            knn.predict_classification(self.X_test_class)
        self.assertIn("Model must be fitted", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            regression_predictor = knn.get_regression_predictor()
            regression_predictor.predict(self.X_test_reg)
        self.assertIn("Model must be fitted", str(context.exception))
    
		# TODO: Add other tests if you'd like
	
    def test_k_larger_than_training_data(self):
        """Test behavior when k is larger than the number of training samples."""
        # Create small training set
        small_X = np.array([[1, 1], [2, 2], [3, 3]])
        small_y = np.array([0, 1, 0])
        
        for k in [5, 10, 15]:  # k larger than training data
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(small_X, small_y)
                
                # Should still work, just use all available neighbors
                predictions = knn.predict_classification(np.array([[1.5, 1.5]]))
                self.assertEqual(len(predictions), 1)
                self.assertIn(predictions[0], [0, 1])
    
		# TODO: Add other tests if you'd like
	
    def test_k_values_consistency(self):
        """Test that the algorithm produces consistent results for the same k value."""
        for k in [1, 3, 5, 7]:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(self.X_train_class, self.y_train_class)
                
                # Make predictions multiple times
                predictions1 = knn.predict_classification(self.X_test_class)
                predictions2 = knn.predict_classification(self.X_test_class)
                predictions3 = knn.predict_classification(self.X_test_class)
                
                np.testing.assert_array_equal(predictions1, predictions2)
                np.testing.assert_array_equal(predictions2, predictions3)
    
		# TODO: Add other tests if you'd like
	
    def test_neighbors_info_method(self):
        """Test the get_neighbors_info method for debugging capabilities."""
        for k in [1, 3, 5]:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(self.X_train_class, self.y_train_class)
                
                neighbors_info = knn.get_neighbors_info(self.X_test_class)
                
                # Verify structure
                self.assertEqual(len(neighbors_info), len(self.X_test_class))
                
                for test_point_neighbors in neighbors_info:
                    # Each test point should have at most k neighbors
                    self.assertLessEqual(len(test_point_neighbors), k)
                    
                    # Each neighbor should be a tuple of (distance, index, label)
                    for neighbor in test_point_neighbors:
                        self.assertEqual(len(neighbor), 3)
                        distance, idx, label = neighbor
                        self.assertIsInstance(distance, (int, float))
                        self.assertIsInstance(idx, (int, np.integer))
                        self.assertIn(label, self.y_train_class)
    
		# TODO: Add other tests if you'd like
	
    def test_empty_training_data(self):
        """Test behavior with empty training data."""
        knn = SimpleKnnAlgorithm(k=3)
        
        # Test with empty arrays
        empty_X = np.array([]).reshape(0, 2)
        empty_y = np.array([])
        
        knn.fit(empty_X, empty_y)
        
        # Should handle empty training data gracefully
        predictions = knn.predict_classification(self.X_test_class)
        self.assertEqual(len(predictions), len(self.X_test_class))
    
		# TODO: Add other tests if you'd like
	
    def test_multiclass_classification(self):
        """Test classification with more than 2 classes."""
        # Create multiclass data
        X_multiclass = np.array([
            [1, 1], [1, 2], [2, 1], [2, 2],  # Class 0
            [5, 5], [5, 6], [6, 5], [6, 6],  # Class 1
            [9, 9], [9, 10], [10, 9], [10, 10]  # Class 2
        ])
        y_multiclass = np.array([0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2])
        
        for k in [1, 3, 5]:
            with self.subTest(k=k):
                knn = SimpleKnnAlgorithm(k=k)
                knn.fit(X_multiclass, y_multiclass)
                
                test_points = np.array([[1.5, 1.5], [5.5, 5.5], [9.5, 9.5]])
                predictions = knn.predict_classification(test_points)
                
                self.assertEqual(len(predictions), 3)
                for pred in predictions:
                    self.assertIn(pred, [0, 1, 2])
    
		# TODO: Add other tests if you'd like
	
    def test_weighted_regression_different_from_mean(self):
        """Test that weighted regression produces different results from simple mean."""
        knn = SimpleKnnAlgorithm(k=3)
        knn.fit(self.X_train_reg, self.y_train_reg)
        
        regression_predictor = knn.get_regression_predictor()
        
        mean_predictions = regression_predictor.predict(self.X_test_reg, 'mean')
        weighted_predictions = regression_predictor.predict(self.X_test_reg, 'weighted_mean')
        
        # At least some predictions should be different
        differences = np.abs(mean_predictions - weighted_predictions)
        self.assertTrue(np.any(differences > 0.1), 
                       "Weighted mean should produce different results from simple mean")

		# TODO: Add other tests if you'd like	

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
