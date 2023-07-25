import pandas as pd
import unittest
from datetime import datetime
from main import StockTrade

class StockTradeTests(unittest.TestCase):

    def setUp(self):
        self.stock_trade = StockTrade()

    def test_perform_trading(self):
        self._add_record()
        self.trade_data = self.stock_trade.get_recorded_trade()
        print(self.trade_data)

    def _add_record(self):
        self.stock_trade.record_trade(
            datetime(2023, 7, 25, 4, 0, 0).strftime("%m-%d-%Y %H:%M:%S"), 'TEA', 'Buy', 4, 300)
        self.stock_trade.record_trade(
            datetime(2023, 7, 25, 4, 5, 0).strftime(("%m-%d-%Y %H:%M:%S")), 'POP', 'Buy', 8, 200)
        self.stock_trade.record_trade(
            datetime(2023, 7, 25, 4, 5, 0).strftime(("%m-%d-%Y %H:%M:%S")), 'TEA', 'Sell', 1, 100)
        self.stock_trade.record_trade(
            datetime(2023, 7, 25, 4, 5, 0).strftime(("%m-%d-%Y %H:%M:%S")), 'ALE', 'Buy', 10, 150)
        self.stock_trade.record_trade(
            datetime(2023, 7, 25, 4, 5, 0).strftime(("%m-%d-%Y %H:%M:%S")), 'POP', 'Sell', 3, 80)
        self.stock_trade.record_trade(
            datetime(2023, 7, 25, 4, 5, 0).strftime(("%m-%d-%Y %H:%M:%S")), 'TEA', 'Buy', 15, 50)

if __name__ == '__main__':
    unittest.main()
