# indicators.py
import pandas as pd
import pandas_ta as ta


def calculate_indicators(bars_df):
    """
    输入 Alpaca 的 K 线 DataFrame，返回计算好指标的 DataFrame
    """
    if bars_df.empty:
        return bars_df

    # 1. 计算 MACD (12, 26, 9)
    macd = bars_df.ta.macd(close='close', fast=12, slow=26, signal=9)

    # 2. 计算 RSI (14)
    rsi = bars_df.ta.rsi(close='close', length=14)

    # 3. 计算 Momentum (10) -> 当前价减去10分钟前的价
    mom = bars_df.ta.mom(close='close', length=10)

    # 将指标合并到原始数据中
    df = pd.concat([bars_df, macd, rsi, mom], axis=1)
    return df


def check_resonance_signal(df):
    """
    检查倒数第二根K线（刚确立的一分钟）是否触发三强共振
    """
    if len(df) < 3:
        return False, 0.0

    latest = df.iloc[-2]
    prev = df.iloc[-3]
    current_close = latest['close']

    # 提取 MACD 信号
    macd_gold_cross = (latest['MACD_12_26_9'] > latest['MACDS_12_26_9']) and (
                prev['MACD_12_26_9'] <= prev['MACDS_12_26_9'])

    # 提取 RSI 信号 (大于 50 且向上)
    rsi_positive = (latest['RSI_14'] > 50) and (latest['RSI_14'] > prev['RSI_14'])

    # 提取 Momentum 信号 (大于 0 且向上)
    mom_positive = (latest['MOM_10'] > 0) and (latest['MOM_10'] > prev['MOM_10'])

    # 三强共振触发
    if macd_gold_cross and rsi_positive and mom_positive:
        return True, current_close

    return False, current_close