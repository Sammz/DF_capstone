import pandas as pd
from etl.transform.clean_house_price_data import transform_house_price_data


def transform_data(data) -> pd.DataFrame:
    return transform_house_price_data(data)
