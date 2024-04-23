def generate_statement_request_url(
    statement_type: str,
    ticker: str,
    period: str = "annual",
    limit: str = "10",
    api_key: str = None,
) -> str:
    """
    Generates a URL to fetch data from the Financial Modeling Prep API.

    Args:
        statement_type (str): The type of financial statement data to fetch. Valid
            inputs are 'bs', 'is, 'cfs', and 'metrics'.

    Returns:
        str: The URL for the requested data.

    Raises:
        ValueError: If an invalid data type is provided.
    """
    fmp_template = (
        "https://financialmodelingprep.com/api/v3/{}/{}?period={}&limit={}&apikey={}"
    )

    validate_request_statement_type(statement_type)
    validate_period(period)
    validate_limit(limit)
    validate_api_key(api_key)
    validate_ticker(ticker)
    statement_string = generate_statement_string(statement_type)

    return fmp_template.format(statement_string, ticker.upper(), period, limit, api_key)


def generate_stock_list_url(api_key: str) -> str:
    """
    Generates the URL to fetch the list of stock tickers.

    Args:
        api_key (str): The API key to use when fetching data.

    Returns:
        str: The URL to fetch the list of stock tickers.
    """
    validate_api_key(api_key)
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"
    return url


def validate_request_statement_type(statement_type: str) -> None:
    """
    Validates the statement type provided by the user.

    Args:
        statement_type (str): The type of financial statement data to fetch.

    Returns:
        None

    Raises:
        ValueError: If an invalid data type is provided.
    """
    valid_types = ["bs", "is", "cfs", "metrics"]
    if statement_type not in valid_types:
        err_msg = f"{statement_type} is not a valid statement type"
        raise ValueError(err_msg)


def validate_period(period: str) -> None:
    """
    Validates the period provided by the user.

    Args:
        period (str): The period for which to fetch financial data.

    Returns:
        None

    Raises:
        ValueError: If an invalid period is provided.
    """
    valid_periods = ["annual", "quarter"]
    if period not in valid_periods:
        err_msg = f"{period} is not a valid period"
        raise ValueError(err_msg)


def validate_limit(limit: str | int) -> None:
    """
    Validates the limit provided by the user.

    Args:
        limit (str): The number of data points to fetch.

    Returns:
        None

    Raises:
        ValueError: If an invalid limit is provided.
    """
    limit = str(limit)
    if not limit.isdigit():
        err_msg = f"{limit} is not a valid limit"
        raise ValueError(err_msg)


def validate_api_key(api_key: str) -> None:
    """
    Validates the API key provided by the user.

    Args:
        api_key (str): The API key to use when fetching data.

    Returns:
        None

    Raises:
        ValueError: If an invalid API key is provided.
    """
    if not isinstance(api_key, str):
        err_msg = "API key must be a string"
        raise ValueError(err_msg)


def validate_ticker(ticker: str) -> None:
    """
    Validates the ticker provided by the user.

    Args:
        ticker (str): The ticker symbol for the company to fetch data for.

    Returns:
        None

    Raises:
        ValueError: If an invalid ticker is provided.
    """
    if not isinstance(ticker, str):
        err_msg = "ticker must be a string"
        raise ValueError(err_msg)


def generate_statement_string(statement_type: str) -> str:
    """
    Generates a string to represent the type of financial statement data to fetch.

    Args:
        statement_type (str): The type of financial statement data to fetch.

    Returns:
        str: The string representation of the statement type.

    Raises:
        ValueError: If an invalid data type is provided.
    """
    if statement_type == "bs":
        return "balance-sheet-statement"
    elif statement_type == "is":
        return "income-statement"
    elif statement_type == "cfs":
        return "cash-flow-statement"
    elif statement_type == "metrics":
        return "key-metrics"
    else:
        err_msg = f"{statement_type} is not a valid statement type"
        raise ValueError(err_msg)


if __name__ == "__main__":
    # Example usage
    statement_type = "bs"
    ticker = "AAPL"
    period = "annual"
    limit = "10"
    api_key = "1234"
    print(
        generate_statement_request_url(statement_type, ticker, period, limit, api_key)
    )
    print(generate_stock_list_url(api_key))
