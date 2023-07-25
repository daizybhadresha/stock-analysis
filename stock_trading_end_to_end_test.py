import pandas as pd
import unittest
from datetime import datetime
from stock_trade import StockTrade

class StockTradeTests(unittest.TestCase):

    def setUp(self):
        self.stock_trade = StockTrade()

    def test_main(self):
        keep_menu_enabled = True
        while keep_menu_enabled:
            self.provide_options()
            option = input("Enter the option number: \n")
            if option == '6':
                keep_menu_enabled = False

            if option == '1':
                symbol = input("Enter the stock symbol : ")
                old = input("Is this any old (Y/N) : ")
                if old == 'Y':
                    timestamp = input("Enter date time in format mm-mm-yyyy H:M:S :" )
                else:
                    timestamp = None
                trans_type = input("Buy/Sell : ")
                quantity = input("Enter quantity of stocks : ")
                trade_price = input("Enter price : ")
                self.stock_trade.record_trade(timestamp, symbol, trans_type, quantity, trade_price)
                self.stock_trade.get_recorded_trade()

            if option == '2':
                symbol = input("Enter the stock symbol : ")
                trade_price = input("Enter price : ")
                dividend = self.stock_trade.calculate_dividend(symbol, float(trade_price))
                if dividend:
                    print("Calculated dividend: ", dividend)

            if option == '3':
                symbol = input("Enter the stock symbol : ")
                trade_price = input("Enter price : ")
                pe_ratio = self.stock_trade.calculate_pe_ratio(symbol, float(trade_price))
                if pe_ratio:
                    print("Calculated price to earnings ratio: ", pe_ratio)

            if option == '4':
                symbol = input("Enter the stock symbol : ")
                vwsp = self.stock_trade.volume_weighted_stock_price(symbol)
                print("Calculates Volume Weighted Stock Price based on trades in past 15 minutes: ", vwsp)

            if option == '5':
                all_share_index = self.stock_trade.calculate_all_share_index()
                print("Calculated All share index: ", all_share_index)


    def provide_options(self):
        print("------------MENU---------------\n")
        print("1 - Add trade transaction\n")
        print("2 - Calculate dividend\n")
        print("3 - Calculate P/E Ratio\n")
        print("4 - Calculate volume weighted stock for the past 15 minutes\n")
        print("5 - Calculate all share index\n")
        print("6 - Exit\n")
        print("-------------------------------\n")

if __name__ == '__main__':
    unittest.main()
