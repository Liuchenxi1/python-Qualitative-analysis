import unittest
import os
from alpaca.trading.client import TradingClient
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.enums import DataFeed
from alpaca.data.timeframe import TimeFrame
import datetime
import config as config

def test_alpaca_connection():
    """
    Test the connection with Alpaca connection to ensure API key and secret works
    :return: PASS
    """
    assert config.API_KEY, "API_KEY is missing"
    assert config.SECRET_KEY, "SECRET_KEY is missing"

    client = TradingClient(
        config.API_KEY,
        config.SECRET_KEY,
        paper=True,
    )

def test_market_data_is_returned():
    client = StockHistoricalDataClient(
        api_key=config.API_KEY,
        secret_key=config.SECRET_KEY,
    )

    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=7)

    request = StockBarsRequest(
        symbol_or_symbols="AAPL",
        timeframe=TimeFrame.Day,
        start=start_time,
        end=end_time,
        feed=DataFeed.IEX,
    )

    bars = client.get_stock_bars(request)

    assert "AAPL" in bars.data
    assert len(bars.data["AAPL"]) > 0
    assert bars.data["AAPL"][0].close > 0