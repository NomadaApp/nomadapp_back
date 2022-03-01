import unittest
from nomadapp-back import greetings as grt

class TestSpreadsheetApi(unittest.TestCase):
    def test_hello(self):
        grt.hello()
        self.assertEqual(True, True, 'I leave Python!')

if __name__ == '__main__':
    unittest.main()

