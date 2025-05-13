import os
import pandas as pd
import logging
from sqlalchemy import text, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker
from config.db_config import load_db_config, DatabaseConfigError
from utils.db_utils import (
    get_db_connection,
    DatabaseConnectionError,
    QueryExecutionError,
)
from utils.file_utils import QUERY_PATH
from utils.logging_utils import setup_logger
from utils.sql_utils import import_sql_query

SCHEMA = 'c12de'
TARGET_TABLE_NAME = "demo_sam_uk_house_prices_2025"


# Configure the logger
logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


LOAD_QUERY_FILES = {
    "set_primary_key": os.path.join(
        os.path.dirname(QUERY_PATH), "sql/set_primary_key.sql"
    ),
}


def load_data(data: pd.DataFrame):
    # Save data to an SQL table in target database
    create_uk_house_prices_2025_table(data)

    return None


def create_uk_house_prices_2025_table(data: pd.DataFrame):
    try:
        connection_details = load_db_config()["target_database"]
        connection = get_db_connection(connection_details)
        data.to_sql(TARGET_TABLE_NAME, connection,
                    schema=SCHEMA, if_exists="fail", index=False)
        set_primary_key(connection)
    except ValueError:
        logger.setLevel(logging.WARNING)
        logger.warning("Target table exists")
        logger.setLevel(logging.INFO)
        logger.info("Upserting data into existing table instead")
        upsert_on_existing_table(data, connection)
    except DatabaseConfigError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Target database not configured correctly: {e}")
        raise
    except DatabaseConnectionError as e:
        logger.setLevel(logging.ERROR)
        logger.error(
            f"Failed to connect to the database when creating table:"
            f" {e}"
        )
        raise
    except pd.errors.DatabaseError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Failed to create data table: {e}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
    finally:
        connection.close()
        logger.info("Successfully closed database connection.")


def upsert_on_existing_table(data: pd.DataFrame, connection):
    try:
        data_dict = data.to_dict(orient="records")

        # Reflect the table from the database
        metadata = MetaData()
        table = Table(TARGET_TABLE_NAME, metadata, schema=SCHEMA,
                      autoload_with=connection)

        # Create an insert statement with an upsert (ON CONFLICT) clause
        insert_stmt = insert(table).values(data_dict)
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["transaction_id"],
            set_={
                col.name: insert_stmt.excluded[col.name]
                for col in table.columns
                if col.name != "transaction_id"
            },
        )

        # Log the SQL statement and parameters
        logger.debug(
            f"Upsert statement: {str(upsert_stmt.compile(
                dialect=connection.dialect
            ))}"
        )
        logger.debug(f"Parameters: {data_dict}")

        # Create a session
        Session = sessionmaker(bind=connection)
        session = Session()

        # # Execute the upsert statement within a transaction
        session.execute(upsert_stmt)
        # session.commit()
    except SQLAlchemyError as e:
        if "session" in locals():
            session.rollback()
        logger.setLevel(logging.ERROR)
        logger.error(f"Failed to upsert data into {TARGET_TABLE_NAME}: {e}")
        raise QueryExecutionError(f"Failed to execute upsert query: {e}")
    except Exception as e:
        if "session" in locals():
            session.rollback()
        logger.setLevel(logging.ERROR)
        logger.error(f"An error occurred when upserting data: {e}")
        raise
    finally:
        if "session" in locals():
            session.close()
        logger.info("Successfully closed database session.")


def set_primary_key(connection):
    create_primary_key_query = import_sql_query(
        LOAD_QUERY_FILES["set_primary_key"]
    )
    logger.debug(create_primary_key_query)
    executable_sql = text(create_primary_key_query)
    try:
        with connection.begin():
            connection.execute(executable_sql)
            logger.info("Primary key set on target table")
            connection.commit()
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error setting primary key on target table: {e}")
        raise
