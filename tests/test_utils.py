import unittest
from nomadapp_back import utils
import pandas as pd


class TestUtils(unittest.TestCase):
    def test_distance_from_location(self):
        tolerance = 0.01

        lat_1, lon_1 = 40, 40
        lat_2, lon_2 = 50, 50
        known_distance = 1358  # https://www.nhc.noaa.gov/gccalc.shtml

        d12 = utils.distance_from_location((lat_1, lon_1), (lat_2, lon_2))

        absolute_error = abs(known_distance - d12)
        relative_error = absolute_error / max(known_distance, d12)

        self.assertLessEqual(
            relative_error, tolerance, "Wrong GPS Distance Calculation"
        )

    def test_distance_column(self):
        query_df = pd.DataFrame()
        lat = 50
        lon = 50
        lats = [40, 41, 42, 43, 44, 45]
        lons = [40, 41, 42, 43, 44, 45]

        query_df["lat"] = pd.Series(lats)
        query_df["lon"] = pd.Series(lons)

        coordinates = {"lat": 50, "lon": 50}
        res = utils.create_distance_column(query_df, coordinates)
        expected_res = []
        for i in range(len(lats)):
            expected_res.append(
                utils.distance_from_location((lats[i], lons[i]), (lat, lon))
            )
        # self.assertEqual(res, expected_res, "Dataframe is not the one expected!")
        self.assertEqual(res, expected_res, "Dataframe is not the one expected!")


if __name__ == "__main__":
    unittest.main()
