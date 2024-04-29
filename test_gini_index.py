import unittest
from gini_index import get_gini_index
from gini_index import float_to_int

class TestGiniIndex(unittest.TestCase):
    def test_get_gini_index(self):
        # Arrange
        expected = 200
        
        # Act
        status_code, result = get_gini_index()
        
        # Assert
        self.assertEqual(status_code, expected)

    def test_float_to_int_negative(self):
        # Arrange
        value = -2.3
        
        # Act
        result = float_to_int(value)
        
        # Assert
        self.assertEqual(result, -1)
    
    def test_float_to_int_flooring(self):
        # Arrange
        value = 1.44
        
        # Act
        result = float_to_int(value)
        
        # Assert
        self.assertEqual(result, 2)

    def test_float_to_int_ceiling(self):
        # Arrange
        value = 2.55
        
        # Act
        result = float_to_int(value)
        
        # Assert
        self.assertEqual(result, 3)
        
if __name__ == '__main__':
    unittest.main()