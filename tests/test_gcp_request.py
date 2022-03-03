import unittest
import requests
from nomadapp_back import flask_api


class TestGCPRequest(unittest.TestCase):
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

        response = requests.get(url, params=query)
        self.assertEqual(
            response.status_code, 200, f"I get an error {response.status_code}"
        )


if __name__ == "__main__":
    unittest.main()
