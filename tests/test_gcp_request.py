import unittest
import requests


class TestGCPRequest(unittest.TestCase):
    def test_hello(self):
        url = "https://nomadapp-back-akukb5qdcq-ew.a.run.app/json-request"
        # response = requests.get(url, json=None)
        # self.assertEqual({"test": 1}, response.json(), "I leave Python!")


if __name__ == "__main__":
    unittest.main()
