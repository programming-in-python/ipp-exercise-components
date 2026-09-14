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
    from ipp.exercises.labmodule09.simple_weather_predictor import SimpleWeatherPredictor
    MODULE_AVAILABLE = True
except ImportError:
    MODULE_AVAILABLE = False

SKIP_REASON = (
    "Solution not yet implemented. Create "
    "ipp/exercises/labmodule09/simple_weather_predictor.py."
)


@unittest.skipUnless(MODULE_AVAILABLE, SKIP_REASON)
class SimpleWeatherPredictorTest(unittest.TestCase):
    """
    Unit tests for SimpleWeatherPredictor class.
    Tests basic functionality of weather prediction using KNN algorithm.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        Creates sample weather history data for testing.
        """
        self.predictor = SimpleWeatherPredictor(k = 3)
        
        # Create sample weather history with at least 3 records
        self.weather_history = [
            {'temperature': 20.0, 'humidity': 65.0, 'pressure': 1013.0},
            {'temperature': 22.0, 'humidity': 60.0, 'pressure': 1015.0},
            {'temperature': 24.0, 'humidity': 55.0, 'pressure': 1017.0},
            {'temperature': 26.0, 'humidity': 50.0, 'pressure': 1019.0},
            {'temperature': 28.0, 'humidity': 45.0, 'pressure': 1021.0}
        ]
    
    def test_prepare_training_data(self):
        """
        Test that training data is prepared correctly from weather history.
        Should create feature-target pairs using sliding window approach.
        """
        training_data = self.predictor.prepare_training_data(self.weather_history)
        
        # Should have data for all three metrics
        self.assertIn('temperature', training_data)
        self.assertIn('humidity', training_data)
        self.assertIn('pressure', training_data)
        
        # With 5 records, we should have 3 training samples (records 3-5)
        self.assertEqual(len(training_data['temperature']), 3)
        self.assertEqual(len(training_data['humidity']), 3)
        self.assertEqual(len(training_data['pressure']), 3)
    
        # TODO: Add other tests if you'd like
    
    def test_train_model(self):
        """
        Test that the predictor can be trained successfully.
        After training, is_trained flag should be True.
        """
        success = self.predictor.train(self.weather_history)
        
        self.assertTrue(success)
        self.assertTrue(self.predictor.is_trained)
        self.assertEqual(self.predictor.training_count, 1)
    
        # TODO: Add other tests if you'd like
    
    def test_predict_after_training(self):
        """
        Test that predictions can be made after training.
        Predictions should return numeric values for all metrics.
        """
        self.predictor.train(self.weather_history)
        
        # Use last 2 records for prediction
        recent_data = self.weather_history[-2:]
        predictions = self.predictor.predict(recent_data)
        
        # Should have predictions for all metrics
        self.assertIsNotNone(predictions['temperature'])
        self.assertIsNotNone(predictions['humidity'])
        self.assertIsNotNone(predictions['pressure'])
        
        # Predictions should be numeric
        self.assertIsInstance(predictions['temperature'], (int, float))
        self.assertIsInstance(predictions['humidity'], (int, float))
        self.assertIsInstance(predictions['pressure'], (int, float))
    
        # TODO: Add other tests if you'd like
    
    def test_predict_without_training(self):
        """
        Test that prediction fails gracefully when model is not trained.
        Should return None values for all predictions.
        """
        recent_data = self.weather_history[-2:]
        predictions = self.predictor.predict(recent_data)
        
        # Should return None for all predictions when not trained
        self.assertIsNone(predictions['temperature'])
        self.assertIsNone(predictions['humidity'])
        self.assertIsNone(predictions['pressure'])
    
        # TODO: Add other tests if you'd like
    
    def test_evaluate_predictions(self):
        """
        Test that prediction evaluation produces error metrics.
        Should return evaluation dictionary with error measurements.
        """
        self.predictor.train(self.weather_history)
        
        # Make predictions
        recent_data = self.weather_history[-2:]
        predictions = self.predictor.predict(recent_data)
        
        # Actual values (last record in history)
        actual = self.weather_history[-1]
        
        # Evaluate predictions
        evaluation = self.predictor.evaluate_predictions(predictions, actual)
        
        # Should have evaluation for all metrics
        self.assertIn('temperature', evaluation)
        self.assertIn('humidity', evaluation)
        self.assertIn('pressure', evaluation)
        
        # Each evaluation should have error metrics
        for metric_eval in evaluation.values():
            self.assertIn('absolute_error', metric_eval)
            self.assertIn('percent_error', metric_eval)

        # TODO: Add other tests if you'd like
    

if __name__ == '__main__':
    unittest.main()
