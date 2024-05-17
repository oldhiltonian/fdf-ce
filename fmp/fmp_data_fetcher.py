import os
from typing import Dict, Tuple

import pandas as pd

from .fmp_urls import (
    generate_statement_request_url,
    generate_statement_string,
    generate_stock_list_url,
)

api_key = os.getenv("FMP_API_KEY")


def fetch_available_companies() -> Tuple[list, list, list]:
    """
    Fetches a list of available companies from the FMP API, filters for stocks,
    and returns lists of ticker symbols, company names, and combined dropdown
    strings.

    Returns:
    A tuple containing three lists:
    1. A list of ticker symbols for available companies.
    2. A list of company names for available companies.
    3. A list of combined dropdown strings for available companies.

    Raises:
    AssertionError: If the lengths of the returned lists do not match.
    """
    url = generate_stock_list_url(api_key)
    df = pd.read_json(url)
    df = df[df["type"] == "stock"]
    df.drop(columns=["price", "exchange", "type"], inplace=True)
    df.dropna(inplace=True)
    df["dropdown"] = df["symbol"] + "  --  " + df["name"]
    tickers = df["symbol"].tolist()
    names = df["name"].tolist()
    dropdowns = df["dropdown"].tolist()
    assert len(tickers) == len(names) == len(dropdowns)
    return tickers, names, dropdowns


def generate_financial_statement_dfs(ticker: str) -> Dict[str, pd.DataFrame]:
    """
    Generate a dictionary of pandas DataFrames containing financial statements
    for the given ticker.

    Parameters:
    ticker (str): The stock ticker symbol for which to retrieve financial
    statements.

    Returns:
    dict: A dictionary where the keys are statement types (e.g., "is", "bs",
        "cfs", "metrics") and the values are pandas DataFrames containing the
        corresponding financial statements.

    The function retrieves financial statements for the specified ticker from
    the FMP API for the following statement types: "is", "bs", "cfs", and
    "metrics". It retrieves annual financial statements with a limit of 10
    statements. The function returns a dictionary where the keys are the
    statement types and the values are pandas DataFrames containing the
    corresponding financial statements.
    """
    statement_data_dict = dict()
    statement_types = ["is", "bs", "cfs", "metrics"]
    for statement_type in statement_types:
        url = generate_statement_request_url(
            statement_type, ticker, period="annual", limit=10, api_key=api_key
        )
        statement_key = ticker + "_" + generate_statement_string(statement_type)
        data_df = pd.read_json(url).transpose()
        data_df = data_df.iloc[:, ::-1]
        statement_data_dict[statement_key] = data_df
    return statement_data_dict


def create_string_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new column in the DataFrame that combines the values of two
    existing columns.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with a new column that combines the values
        of two existing columns.

    The function takes a DataFrame as input and creates a new column called
    "String_Col" that combines the values of two existing columns, "Col1" and
    "Col2". The new column is created by concatenating the values of "Col1" and
    "Col2" with a space between them.
    """
    df["Dropdown"] = df["symbol"] + "-" + df["name"]
    return df


if __name__ == "__main__":
    df = fetch_available_companies()
    print(df)

    dfs = generate_financial_statement_dfs("AAPL")
    for statement_type, df in dfs.items():
        print(statement_type)
        print(df)
