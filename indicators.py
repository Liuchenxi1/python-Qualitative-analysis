# indicators.py
import pandas as pd
import pandas_ta as ta


def calculate_indicators(bars_df):
    """
    input Alpaca candlestick dataframe and return computed indicators
    """
    if bars_df.empty:
        return bars_df

    # 1. MACD (12, 26, 9)
    macd = bars_df.ta.macd(close='close', fast=12, slow=26, signal=9)

    # 2. RSI (14)
    rsi = bars_df.ta.rsi(close='close', length=14)

    # 3. Momentum (10)
    mom = bars_df.ta.mom(close='close', length=10)

    # put the indexes into df
    df = pd.concat([bars_df, macd, rsi, mom], axis=1)
    return df


def check_resonance_signal(df):
    """
    checking the second candlestick signal if the 3 indexes send strong signal
    """
    if len(df) < 3:
        return False, 0.0

    latest = df.iloc[-2]
    prev = df.iloc[-3]
    current_close = latest['close']

    # MACA signal
    macd_gold_cross = (latest['MACD_12_26_9'] > latest['MACDs_12_26_9']) and (
                prev['MACD_12_26_9'] <= prev['MACDs_12_26_9'])

    # RSI signal; RSI >50
    rsi_positive = (latest['RSI_14'] > 50) and (latest['RSI_14'] > prev['RSI_14'])

    # Momentum >0 || Momentum up swig
    mom_positive = (latest['MOM_10'] > 0) and (latest['MOM_10'] > prev['MOM_10'])

    # 3 indexes all fit the requirements
    if macd_gold_cross and rsi_positive and mom_positive:
        return True, current_close

    return False, current_close