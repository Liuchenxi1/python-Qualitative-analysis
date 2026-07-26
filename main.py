# main.py
import alpaca_trade_api as tradeapi
from alpaca.data.historical import StockHistoricalDataClient
import config
from indicators import calculate_indicators, check_resonance_signal
from options import get_best_itm_call
import time

# access Alpaca API
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

SYMBOL = "AAPL"


def run_bot():
    print(f"Bot starts, focusing on {SYMBOL}...")

    while True:
        try:
            # 1. take the lastest 1M candles chart from Alpaca
            bars = api.get_bars(SYMBOL, tradeapi.TimeFrame.Minute, limit=50).df

            # 2. compute 3 indexes
            df_with_indicators = calculate_indicators(bars)

            # 3. checking the trend
            is_triggered, current_price = check_resonance_signal(df_with_indicators)

            if is_triggered:
                print(f"{SYMBOL} has strong up swing tread signal, Stock price right: ${current_price}")

                # 4. scanning the option chain
                best_option = get_best_itm_call(api, SYMBOL, current_price)
                if best_option:
                    print(
                        f"[ITM] The best option price: {best_option['symbol']} | strike: ${best_option['strike']} | expired date: {best_option['expiration']}")
                else:
                    print("⚠ There is no ITM valuable option")

            else:
                print(f"scanning: ${bars.iloc[-1]['close'] if not bars.empty else 'unknown'}，indexes does not matched")

            # running every 60 seconds
            time.sleep(60)

        except Exception as e:
            print(f"running failed: {e}")
            time.sleep(10)


if __name__ == "__main__":
    run_bot()
