# test_indicators_mock.py
import unittest
import pandas as pd
import numpy as np
from indicators import calculate_indicators, check_resonance_signal


class TestIndicatorsResonance(unittest.TestCase):

    def test_mock_resonance_trigger(self):
        """
        手工锻造一段 K 线数据，测试三强共振算法的敏感度
        """
        print("\n[测试开始] 正在伪造 1M 级别高频 K 线数据...")

        # 1. 产生 30 根基础 K 线（先让它处于横盘震荡低谷，把指标拉平）
        dates = pd.date_range(start="2026-07-05 09:30:00", periods=30, freq="1min")

        data = {
            "open": [160.0] * 30,
            "high": [160.5] * 30,
            "low": [159.5] * 30,
            "close": [160.0] * 30,  # 收盘价全部横盘
            "volume": [1000] * 30
        }
        mock_df = pd.DataFrame(data, index=dates)
        mock_df.index.name = "timestamp"

        # 2. 重点：开始伪造最后 3 根 K 线，强行制造“买盘加速拉升”
        # 倒数第3根：轻微抬头
        mock_df.iloc[-3, mock_df.columns.get_loc('close')] = 160.5

        # 倒数第2根（触发根）：暴涨！MACD金叉，RSI冲过50，Momentum大转阳
        mock_df.iloc[-2, mock_df.columns.get_loc('close')] = 163.5
        mock_df.iloc[-2, mock_df.columns.get_loc('high')] = 164.0

        # 最后一根（未收盘当前根）：继续维持高位
        mock_df.iloc[-1, mock_df.columns.get_loc('close')] = 163.8

        # 3. 喂入你的核心算法进行计算
        df_with_indicators = calculate_indicators(mock_df)
        print("💡 pandas_ta 算出来的实际列名有：", df_with_indicators.columns.tolist())

        # 4. 检测信号
        is_triggered, trigger_price = check_resonance_signal(df_with_indicators)

        # 5. 验证结果
        print(f"📊 伪造数据计算完毕。倒数第二根K线收盘价: ${trigger_price}")
        print(f"📡 算法共振触发状态: {is_triggered}")

        # 理论上这里必须触发成功
        self.assertTrue(is_triggered, "错误：精心伪造的共振数据竟然没有触发信号！请检查 indicators.py 的阈值判断。")
        print("🎯 [测试通过] 核心指标计算与共振过滤逻辑完全正确！成功识别多头爆发点。")


if __name__ == '__main__':
    unittest.main()