import  unittest
import pandas as pd

from indicators import calculate_indicators, check_resonance_signal

class TestIndicators(unittest.TestCase):

    def test_check_resonance_signal(self):
        dates = pd.date_range(start="2026-07-01", periods=60, freq="1min")

        mock_df = pd.DataFrame({"open": [160.0] * 60,
        "high":[160.5] * 60,
        "low":[159.5] * 60,
        "close":[160.0] * 60,
        "volume": [1000] * 60,},

        index = dates,
                               )
        mock_df.index.name = "timestamp"

        # A small upward move.
        mock_df.iloc[-3] = [160.0, 160.8, 159.9, 160.5, 1500]

        # A strong bullish candle.
        mock_df.iloc[-2] = [160.5, 164.0, 160.4, 163.5, 10000]

        # Latest completed candle: remains bullish.
        mock_df.iloc[-1] = [163.5, 164.2, 163.2, 163.8, 8000]

        df_with_indicators = calculate_indicators(mock_df)

        is_triggered, trigger_price = check_resonance_signal(df_with_indicators)

        self.assertTrue(
            is_triggered,
            "Expected the artificial bullish move to trigger a resonance signal.",
        )
        self.assertIsNotNone(trigger_price)
        self.assertGreater(trigger_price, 0)

