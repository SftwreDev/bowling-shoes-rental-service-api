import logging
from typing import Any, Dict, List, Optional, Union

from app.supabase import create_supabase_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize supabase client
supabase = create_supabase_client()


def retrieve_query(
    table: str, columns: List[str], filters: Optional[Dict[str, Any]] = None
) -> Union[List[Dict[str, Any]], Exception]:
    """Retrieve Data from a Specified Table

    This function retrieves data from a specified table in Supabase, allowing for optional filtering.

    Args:
        table (str): The name of the table to query.
        columns (List[str]): A list of column names to select.
        filters (Optional[Dict[str, Any]]): A dictionary of filter conditions where the key is the column name and the value is the filter value.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the rows returned by the query.

    Raises:
        Exception: If an error occurs during the query execution.
    """
    try:
        # Build the base query
        query = supabase.table(table).select(", ".join(columns))

        # Apply filters if provided
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)

        # Execute the query and return results
        results = query.execute()

        # Check if results are empty and log the event
        if not results.data:
            logger.warning(
                f"No records found in table '{table}' with filters: {filters}"
            )

        logger.info(
            f"Successfully retrieved {len(results.data)} records from table '{table}'."
        )
        return results.data

    except Exception as e:
        # Log the error with details
        logger.error(
            f"An error occurred during the retrieve operation in table '{table}': {e}"
        )
        # Raise a more informative exception
        raise Exception(f"Failed to retrieve data from table '{table}': {str(e)}")


def create_query(
    table: str, data: Dict[str, Any]
) -> Union[List[Dict[str, Any]], Exception]:
    """Inserts data into a specified table in Supabase.

    Args:
        table (str): The name of the Supabase table where data will be inserted.
        data (dict): A dictionary representing the data to insert into the table.

    Returns:
        dict: The response from Supabase containing the result of the insert operation.

    Raises:
        ValueError: If the `table` name or `data` dictionary is invalid.
        Exception: If an error occurs during the Supabase insert operation.
    """
    # Log the beginning of the insert operation
    logger.info(f"Starting insert operation in table '{table}' with data: {data}")

    try:
        # Execute the insert query
        response = supabase.table(table).insert(data).execute()

        # Log successful insertion
        logger.info(f"Successfully inserted data into table '{table}': {response.data}")
        return response.data

    except Exception as e:
        logger.error(
            f"An error occurred during insert operation in table '{table}': {e}"
        )
        raise Exception(e.__dict__.get("message"))
