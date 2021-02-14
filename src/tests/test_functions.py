import unittest
import datetime
from .. import lambda_function


class TestFunctions(unittest.TestCase):

    # 同じ時間(year_to_hour)
    def test_match_for_year_to_hour_same_time(self):
        datetime_a = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        datetime_b = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        self.assertEqual(lambda_function.match_for_year_to_hour(
            datetime_a, datetime_b), True)

    # 違う分(year_to_hour)
    def test_match_for_year_to_hour_diff_minute(self):
        datetime_a = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        datetime_b = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=59, second=29)
        self.assertEqual(lambda_function.match_for_year_to_hour(
            datetime_a, datetime_b), True
        )

    # 違う時間(year_to_hour)
    def test_match_for_year_to_hour_diff_hour(self):
        datetime_a = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        datetime_b = datetime.datetime(
            year=2019, month=12, day=29, hour=15, minute=0, second=29)
        self.assertEqual(lambda_function.match_for_year_to_hour(
            datetime_a, datetime_b), False)

    # 同じ時間(year_to_day)
    def test_match_for_year_to_day_same_hour(self):
        datetime_a = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        datetime_b = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        self.assertEqual(lambda_function.match_for_year_to_day(
            datetime_a, datetime_b), True)

    # 違う日(year_to_day)
    def test_match_for_year_to_day_diff_day(self):
        datetime_a = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        datetime_b = datetime.datetime(
            year=2019, month=12, day=29, hour=14, minute=0, second=29)
        self.assertEqual(lambda_function.match_for_year_to_day(
            datetime_a, datetime_b), False)

    # 違う時間(year_to_day)
    def test_match_for_year_to_day_diff_hour(self):
        datetime_a = datetime.datetime(
            year=2019, month=12, day=30, hour=14, minute=0, second=29)
        datetime_b = datetime.datetime(
            year=2019, month=12, day=30, hour=15, minute=0, second=29)
        self.assertEqual(lambda_function.match_for_year_to_day(
            datetime_a, datetime_b), True)


if __name__ == '__main__':
    unittest.main()
