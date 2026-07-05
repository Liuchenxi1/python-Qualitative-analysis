# options.py
import datetime


def get_best_itm_call(api, symbol, current_price):
    """
    获取离当前价格最近的 ITM（价内）看涨期权
    """
    try:
        # 获取该股票的所有期权合约
        contracts = api.get_option_contracts(symbol)

        # 筛选：选择即将到期的看涨期权（Call），且行权价低于当前股价（即 ITM）
        itm_calls = []
        today = datetime.date.today()

        for c in contracts:
            # 过滤：只要 Call，只要行权价小于当前股价（ITM）
            if c.type == 'call' and c.strike < current_price:
                # 过滤到期日：选择距离今天最近的常规到期日（比如当周五）
                expiration = datetime.datetime.strptime(c.expiration_date, "%Y-%m-%d").date()
                if expiration >= today:
                    itm_calls.append(c)

        if not itm_calls:
            return None

        # 排序：按照行权价从大到小排序，最接近当前股价的就是最优的 ITM Call
        itm_calls.sort(key=lambda x: x.strike, reverse=True)
        best_call = itm_calls[0]

        return {
            "symbol": best_call.symbol,
            "strike": best_call.strike,
            "expiration": best_call.expiration_date
        }
    except Exception as e:
        print(f"获取期权链失败: {e}")
        return None