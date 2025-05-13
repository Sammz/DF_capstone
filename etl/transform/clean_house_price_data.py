import pandas as pd
import logging
from utils.file_utils import save_dataframe_to_csv
from utils.logging_utils import setup_logger

# Configure the logger
logger = setup_logger(
    __name__,
    'extract_data.log',
    level=logging.DEBUG
)

# List of columns where missing values are fine
# An address does not need a Secondary Addressable Object Name
# or locality to be valid
COLUMNS_ALLOWED_TO_HAVE_NULL_VALUES = ['SAON', 'locality']

# Threshold percentage for dropping values to give a warning
WARNING_THRESHOLD = 10


def clean_house_price_data(house_price_data: pd.DataFrame) -> pd.DataFrame:
    # Set transaction_id as the index to become the primary key in the database
    house_price_data.set_index('transaction_id')

    # Parse all dates with pd.to_datetime. Coerce errors means it will put
    # a null value if parsing fails.
    house_price_data['date'] = pd.to_datetime(house_price_data['date'], 
                                              errors='coerce')

    # Remove rows with missing values
    clean_house_price_data = remove_missing_values(house_price_data)

    # give newbuild column type boolean
    clean_house_price_data['newbuild'] = clean_house_price_data['newbuild'].map({'Y': True, 'N': False})

    # Save the dataframe as a CSV for logging purposes
    save_dataframe_to_csv(clean_house_price_data, "etl/data/processed/", 
                          "cleaned_house_price_data.csv",)

    return clean_house_price_data


def remove_missing_values(house_price_data):
    row_count = house_price_data.shape[0]

    for col in house_price_data.columns:
        if col not in COLUMNS_ALLOWED_TO_HAVE_NULL_VALUES:
            null_count = house_price_data[col].isna().sum()
            
            if null_count > 0:
                house_price_data = house_price_data.dropna(subset=col)
                percent_dropped = round(null_count / row_count * 100, 2)
                
                log_message = f'Dropped {null_count} ({percent_dropped}%) rows with missing values in the {col} column.'
                
                if percent_dropped > WARNING_THRESHOLD:
                    logger.setLevel(logging.WARNING)
                    logger.warning(log_message)
                else:
                    logger.setLevel(logging.INFO)
                    logger.info(log_message)

    return house_price_data
