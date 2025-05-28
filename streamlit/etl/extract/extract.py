import pandas as pd
from etl.extract.extract_house_price_data import extract_house_prices


def extract_data() -> pd.DataFrame:
    house_price_data = extract_house_prices()
    return house_price_data
