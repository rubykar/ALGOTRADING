import pandas as pd
import numpy as np

# result_df = pd.read_csv("DailyNifty500.csv")


def find_close_rsi(symbol, date, time, data_6m_hourly):
    """
    Finds the close and RSI values for a given symbol, date, and time.

    Args:
        symbol: The symbol of the stock.
        date: The date in the format 'YYYY-MM-DD'.
        time: The time in the format 'HH:MM:SS'.

    Returns:
        A tuple containing the close and RSI values, or None if no data is found.
    """

    # Convert date and time to appropriate formats
    target_date = pd.to_datetime(date, format="%Y-%m-%d").date()
    target_time = pd.to_datetime(time, format="%H:%M:%S").time()

    # Filter the DataFrame based on the target symbol, date, and time
    filtered_df = data_6m_hourly[
        (data_6m_hourly["Symbol"] == symbol)
        & (data_6m_hourly["date_only"] == target_date)
        & (data_6m_hourly["time_only"] == target_time)
    ]

    # Check if any rows are returned
    if not filtered_df.empty:
        close_value = filtered_df["Close"].iloc[0]
        rsi_value = filtered_df["RSI"].iloc[0]
        high_value = filtered_df["High"].iloc[0]
        return close_value, rsi_value, high_value
    else:
        return 0, 0, 0


import pandas as pd
from datetime import timedelta


def find_next_hour_open(symbol, date, time, data_6m_hourly):
    """
    Finds the open value for the next hour given the symbol, date, and time.

    Args:
        symbol: The symbol of the stock.
        date: The date in the format 'YYYY-MM-DD'.
        time: The time in the format 'HH:MM:SS'.

    Returns:
        The open value for the next hour, or None if no data is found.
    """

    # Convert date and time to appropriate formats
    target_date = pd.to_datetime(date, format="%Y-%m-%d").date()
    target_time = pd.to_datetime(time, format="%H:%M:%S").time()

    next_hour = pd.to_datetime(
        target_date.strftime("%Y-%m-%d") + " " + target_time.strftime("%H:%M:%S")
    ) + timedelta(hours=1)

    filtered_df = data_6m_hourly[
        (data_6m_hourly["Symbol"] == symbol)
        & (data_6m_hourly["date_only"] == target_date)
        & (data_6m_hourly["time_only"] == next_hour.time())
    ]

    # Check if any rows are returned
    if not filtered_df.empty:
        return filtered_df["Open"].iloc[0]
    else:
        return 0


def get_close_day0(symbol, date, result_df):
    try:
        result_df["date"] = pd.to_datetime(result_df["date"])
        row_index = result_df[
            (result_df["symbol"] == symbol)
            & (result_df["date"] == pd.to_datetime(date).strftime("%Y-%m-%d"))
        ].index[0]
        next_close_day1 = result_df.iloc[row_index]["close"]
        return next_close_day1
    except IndexError:
        return np.nan


def get_next_close_day1(symbol, date, result_df):
    try:        
        result_df["date"] = pd.to_datetime(result_df["date"])
        row_index = result_df[
            (result_df["symbol"] == symbol)
            & (result_df["date"] == pd.to_datetime(date).strftime("%Y-%m-%d"))
        ].index[0]
        next_close_day1 = result_df.iloc[row_index + 1]["close"]
        return next_close_day1
    except IndexError:
        return np.nan


def get_next_close_day2(symbol, date, result_df):
    try:
        result_df["date"] = pd.to_datetime(result_df["date"])
        row_index = result_df[
            (result_df["symbol"] == symbol)
            & (result_df["date"] == pd.to_datetime(date).strftime("%Y-%m-%d"))
        ].index[0]
        next_close_day2 = result_df.iloc[row_index + 2]["close"]
        return next_close_day2
    except IndexError:
        return np.nan


def get_next_close_day3(symbol, date, result_df):
    try:
        result_df["date"] = pd.to_datetime(result_df["date"])
        row_index = result_df[
            (result_df["symbol"] == symbol)
            & (result_df["date"] == pd.to_datetime(date).strftime("%Y-%m-%d"))
        ].index[0]
        next_close_day3 = result_df.iloc[row_index + 3]["close"]
        return next_close_day3
    except IndexError:
        return np.nan





# symbol = "SAFARI"
# date = "2024-04-01"

# next_close_day1 = get_next_close_day1(symbol, date, result_df)
# next_close_day2 = get_next_close_day2(symbol, date, result_df)
# next_close_day3 = get_next_close_day3(symbol, date, result_df)

# print(f"Next close for Day 1: {next_close_day1}")
# print(f"Next close for Day 2: {next_close_day2}")
# print(f"Next close for Day 3: {next_close_day3}")
