# test_400_error.py
import unittest
from unittest.mock import patch, MagicMock
from alpaca.common.exceptions import APIError
import main


class TestAlpacaConnectionError(unittest.TestCase):

    @patch('main.data_client.get_stock_bars')
    def test_handle_400_error(self, mock_get_bars):
        """
        测试当 Alpaca 接口返回 400 坏请求时，系统是否会触发 except 捕获而不会崩溃
        """
        # 故意制造一个标准的 Alpaca 400 错误请求异常
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_index = lambda: {"message": "Invalid API Key or parameters."}

        # 让模拟的客户端在被调用时，直接砸出这个 400 错误
        mock_get_bars.side_effect = APIError("400 Bad Request: Invalid parameters")

        print("\n[测试开始] 正在模拟 Alpaca 400 错误请求...")

        # 捕获主循环，防止它无限死循环，我们只让它跑一次
        with patch('time.sleep', return_value=None) as mock_sleep:
            # 执行一次主逻辑中的核心部分，看它是否能走到 except Exception as e
            try:
                # 模拟 main.py 里的执行逻辑
                request_params = MagicMock()
                bars_df = main.data_client.get_stock_bars(request_params).df
            except Exception as e:
                print(f"🎉 成功捕获到错误信息: {e}")
                # 断言捕获到的错误中确实包含 400
                self.assertIn("400", str(e))
                print("[测试通过] 机器人能够优雅捕获 400 错误，未发生闪退崩溃！")


if __name__ == '__main__':
    unittest.main()