"""Helpers Module"""
__docformat__ = "numpy"

import pandas as pd
import certifi
import json
from urllib.request import urlopen

def combine_dataframes(tickers: str | list[str], *args) -> pd.DataFrame:
    """
    Combine the dataframes from different companies of the same financial statement,
    e.g. the balance sheet statement, into a single dataframe.

    Args:
        **args: A dictionary of the same type of financial statement from multiple companies.

    Returns:
        pd.DataFrame: A pandas DataFrame with the combined financial statements.
    """
    ticker_list = tickers if isinstance(tickers, list) else [tickers]
    combined = zip(ticker_list, args)
    combined_df = pd.concat(dict(combined), axis=0)

    return combined_df.sort_index(level=0, sort_remaining=False)

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def handle_errors(func):
    """
    Decorator to handle specific errors that may occur in a function and provide informative messages.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        KeyError: If an index name is missing in the provided financial statements.
        ValueError: If an error occurs while running the function, typically due to incomplete financial statements.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            function_name = func.__name__
            print(
                "There is an index name missing in the provided financial statements. "
                f"This is {e}. This is required for the function ({function_name}) "
                "to run. Please fill this column to be able to calculate the ratios."
            )
            return pd.Series()
        except ValueError as e:
            function_name = func.__name__
            print(
                f"An error occurred while trying to run the function "
                f"{function_name}. This is {e}. Usually this is due to incomplete "
                "financial statements. "
            )
            return pd.Series()

    return wrapper
