from etl.extract.extract_house_price_data import (
    extract_house_prices,
    EXPECTED_IMPORT_RATE)
from unittest.mock import patch
import time

patch_url = "tests/test_data/test_prices.csv"
url = "etl.extract.extract_house_price_data.yearly_house_price_data_2025_url"


def test_extract_house_prices_returns_all_data():
    expected_shape = (30, 16)

    with patch(url, new=patch_url):
        df = extract_house_prices()

    # Verify the dimensions of the DataFrame
    assert df.shape == expected_shape, (
        f"Expected DataFrame shape to be {expected_shape}, but got {df.shape}")


def test_extract_house_prices_performance():
    start_time = time.time()
    with patch(url, new=patch_url):
        df = extract_house_prices()
    execution_time = time.time() - start_time

    # Mean Time per Row
    actual_execution_time_per_row = execution_time / df.shape[0]

    # Assert that the execution time is within an acceptable range
    assert actual_execution_time_per_row <= EXPECTED_IMPORT_RATE, (
        f"Expected execution time to be less than or equal to "
        f"{str(EXPECTED_IMPORT_RATE)} seconds, but got "
        f"{str(actual_execution_time_per_row)} seconds")


def test_extract_house_prices_handles_malformed_url():

    with patch("etl.extract.extract_house_price_data.logger") as mock_logger:

        malformed_url = 'malform.malform.malform.malform.malform'
        with patch(url, new=malformed_url):

            try:
                extract_house_prices()
            except Exception as e:

                mock_logger.setLevel.assert_called_once()
                mock_logger.error.assert_called_once()
                assert "Error loading from" in mock_logger.error.call_args[0][0]
                assert "Failed to load data from" in str(e)
