import unittest
import requests


class TestGCPRequest(unittest.TestCase):
    def test_hello(self):
        url = "http://localhost/json-request"
        response = requests.get(url, json={"foo": 4})
        self.assertEqual(True, True, "I leave Python!")


if __name__ == "__main__":
    unittest.main()
