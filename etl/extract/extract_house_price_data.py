import pandas as pd
import time
import logging
from utils.logging_utils import setup_logger, log_extract_success


# Configure the logger
logger = setup_logger(
    __name__,
    'extract_data.log',
    level=logging.DEBUG
)

yearly_house_price_data_2025_url = "http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2025.csv"
column_names = ['transaction_id', 'price', 'date', 'postcode', 'property_type', 'newbuild', 'duration', 'PAON', 'SAON', 'street', 'locality', 'city', 'district', 'county', 'ppd_category_type', 'record_status']
 

EXPECTED_IMPORT_RATE = 0.001
TYPE = 'house price data from URL'


def extract_house_prices() -> pd.DataFrame:
    try:
        start_time = time.time()
        dataframe = pd.read_csv(yearly_house_price_data_2025_url, header=None, names=column_names)
        duration = time.time() - start_time
        
        log_extract_success(
                logger,
                TYPE,
                dataframe.shape,
                duration,
                EXPECTED_IMPORT_RATE
            )

        return dataframe

    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading from \"{yearly_house_price_data_2025_url}\": {e}")
        raise Exception(f"Failed to load data from: \"{yearly_house_price_data_2025_url}\"")


    
