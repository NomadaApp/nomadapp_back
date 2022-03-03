import unittest
import requests
from nomadapp_back import flask_api


class TestApiRequest(unittest.TestCase):
    def test_hello(self):
        url = "https://nomadapp-back-akukb5qdcq-ew.a.run.app/json-request"
        query = {
            "leisure": False,
            "restaurants": True,
            "education": True,
            "coworking": False,
            "radius": 5,
            "location": "Puerta del Sol, 1",
        }
        # response = requests.get(url, params=query)
        # url = "https://nomadapp-back-akukb5qdcq-ew.a.run.app/json-request"
        # response = requests.get(url, json=None)
        # self.assertEqual({"test": 1}, response.json(), "I leave Python!")


if __name__ == "__main__":
    unittest.main()
