# main.py
import alpaca_trade_api as tradeapi
from alpaca.data.historical import StockHistoricalDataClient
import config
from indicators import calculate_indicators, check_resonance_signal
from options import get_best_itm_call
import time

# 初始化 Alpaca 客户端
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

SYMBOL = "SPCX"


def run_bot():
    print(f"🚀 交易机器人启动，正在监控 {SYMBOL}...")

    while True:
        try:
            # 1. 从 Alpaca 获取最新的 1分钟 K 线
            bars = api.get_bars(SYMBOL, tradeapi.TimeFrame.Minute, limit=50).df

            # 2. 计算三大指标
            df_with_indicators = calculate_indicators(bars)

            # 3. 检查是否共振
            is_triggered, current_price = check_resonance_signal(df_with_indicators)

            if is_triggered:
                print(f"🚨【信号触发】{SYMBOL} 出现三强共振！当前股价: ${current_price}")

                # 4. 扫描期权链，寻找最契合的 ITM Call
                best_option = get_best_itm_call(api, SYMBOL, current_price)
                if best_option:
                    print(
                        f"🎯【ITM 期权推荐】代码: {best_option['symbol']} | 行权价: ${best_option['strike']} | 到期日: {best_option['expiration']}")
                else:
                    print("⚠️ 未找到合适的 ITM 期权。")

            else:
                print(f"扫描中... 当前价: ${bars.iloc[-1]['close'] if not bars.empty else '未知'}，指标未共振。")

            # 每 60 秒跑一次
            time.sleep(60)

        except Exception as e:
            print(f"运行出错: {e}")
            time.sleep(10)


if __name__ == "__main__":
    run_bot()
