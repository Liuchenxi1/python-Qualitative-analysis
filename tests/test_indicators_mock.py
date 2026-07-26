"""Live one-year MACD crossover report from Alpaca."""

import unittest
from datetime import datetime, timedelta, timezone

from alpaca.data.enums import DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

import config
from indicators import calculate_indicators


SYMBOL = "AAPL"
LOOKBACK_DAYS = 365


def get_one_year_of_daily_bars(symbol=SYMBOL):
    """Return a trailing year of Alpaca daily bars for one symbol."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=LOOKBACK_DAYS)
    client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)
    bars = client.get_stock_bars(
        StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            start=start,
            end=end,
            feed=DataFeed.IEX,
        )
    )
    return bars.df.xs(symbol, level="symbol").sort_index()


def count_macd_crosses(indicators_df):
    """Return (golden_crosses, death_crosses) for the MACD signal line."""
    macd = indicators_df["MACD_12_26_9"]
    signal = indicators_df["MACDs_12_26_9"]
    golden = (macd > signal) & (macd.shift(1) <= signal.shift(1))
    death = (macd < signal) & (macd.shift(1) >= signal.shift(1))
    return int(golden.sum()), int(death.sum())


class TestIndicators(unittest.TestCase):
    def test_one_year_of_alpaca_data_has_indicators_and_cross_counts(self):
        columns = ["MACD_12_26_9", "MACDs_12_26_9", "RSI_14", "MOM_10"]
        self.assertTrue(config.API_KEY, "API_KEY is missing")
        self.assertTrue(config.SECRET_KEY, "SECRET_KEY is missing")
        daily_bars = get_one_year_of_daily_bars()
        self.assertGreaterEqual(len(daily_bars), 200)

        indicators_df = calculate_indicators(daily_bars)
        self.assertTrue(set(columns).issubset(indicators_df.columns))
        self.assertFalse(indicators_df[columns].dropna().empty)

        golden_crosses, death_crosses = count_macd_crosses(indicators_df)
        print(
            f"{SYMBOL} daily MACD crosses for the last {LOOKBACK_DAYS} days: "
            f"{golden_crosses} golden, {death_crosses} death."
        )
        self.assertGreaterEqual(golden_crosses, 0)
        self.assertGreaterEqual(death_crosses, 0)
