import time.time
import pandas as pd
import numpy as np

class StockTrade:

    STOCK_SYMBOL_COL = 'stock_symbol'
    S_STOCK_TYPE_COL = 'stock_type'
    S_LAST_DIVIDEND_COL = 'last_dividend'
    S_FIXED_DIVIDEND_COL = 'fixed_dividend'
    S_PAR_VALUE_COL = 'par_value'
    TYPE_COMMON = 'Common'
    TYPE_PREFERRED = 'Preferred'
    T_TIMESTAMP_COL = 'timestamp'
    T_INDICATOR_COL = 'indicator'
    T_QUANTITY_COL = 'quantity'
    T_TRADED_PRICE_COL = 'traded_price'

    def __init__(self):
        self._trade_data = pd.DataFrame(columns=[T_TIMESTAMP_COL,STOCK_SYMBOL_COL,T_INDICATOR_COL,T_QUANTITY_COL,T_TRADED_PRICE_COL])
        data = [['TEA','Common',0,np.nan,100],['POP','Common',8,np.nan,100],['ALE','Common',23,np.nan,60],
                ['GIN','Preferred',8,2,100],['JOE','Common',13,np.nan,250]]
        self._stock_data = pd.DataFrame(data,
                                columns = [STOCK_SYMBOL_COL,S_STOCK_TYPE_COL,S_LAST_DIVIDEND_COL,S_FIXED_DIVIDEND_COL,S_PAR_VALUE_COL]
                            )

    def record_trade(timestamp, stock_symbol, trans_type, volume, price):
        '''
            Args:
            Returns:
                None
        '''
        if time == None:
            current_time = datetime.now().strftime(("%m-%d-%Y, %H:%M:%S"))
            self._trade_data[T_TIMESTAMP_COL] = current_time
        
        self._trade_data[T_TIMESTAMP_COL] = timestamp
        self._trade_data[STOCK_SYMBOL_COL] = stock_symbol
        self._trade_data[T_INDICATOR_COL] = trans_type
        self._trade_data[T_TRADED_PRICE_COL] = price
        print("A new transaction record added", self._trade_data.tail(1))

    def get_recorded_trade():
        '''
            Args:
            Returns:
                None
        '''
        return self._trade_data

    def load_stock_info(stock_symbol):
        '''
            Args:
            Returns:
                None
        '''
        required_stock = self._stock_data[const.STOCK_SYMBOL == stock_symbol]
        stock_type = required_stock[const.STOCK_TYPE]
        last_dividend = required_stock[const.LAST_DIVIDEND]
        fixed_dividend = required_stock[const.FIXED_DIVIDEND]
        par_value = required_stock[const.PAR_VALUE]
        return stock_type, last_dividend, fixed_dividend, par_value

    def calculate_dividend(self, stock_symbol, stock_price):
        '''
            Args:
            Returns:
                None
        '''
        stock_type, last_dividend, fixed_dividend, par_value = self.load_stock_info(stock_symbol)
        if stock_type == const.TYPE_COMMON:
            dividend = last_dividend/stock_price
        elif stock_type == const.TYPE_PREFERRED:
            dividend = (fixed_dividend * par_value)/stock_price
        else:
            print("Unable to calculate dividend, Encountered unknown stock type")
        return dividend

    def calculate_pe_ratio(stock_symbol, stock_price):
        '''
            Args:
            Returns:
                None
        '''
        dividend = calculate_dividend(stock_symbol, stock_price)
        pe_ratio = stock_price/dividend
        return pe_ratio

    def volume_weighted_stock_price(stock_symbol):
        '''
            Args:
            Returns:
                None
        '''
        timestamp_fifteen_mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
        price_multiply_quantity = 0
        total_quantity = 0
        for row in self._trade_data:
            if row[T_TIMESTAMP_COL] >= timestamp_fifteen_mins_ago and row[STOCK_SYMBOL_COL]==stock_symbol:
                price_multiply_quantity = price_multiply_quantity + (row[T_QUANTITY_COL] * row[T_TRADED_PRICE_COL])
                total_quantity = total_quantity + row[T_QUANTITY_COL]
        
        total_quantity = 1 if total_quantity == 0 else total_quantity
        vwsp = price_multiply_quantity / total_quantity
        return vwsp

    def calculate_all_share_index():
        '''
            Args:
            Returns:
                None
        '''
        all_share_index = np.power(np.prod(self._trade_data[T_TRADED_PRICE_COL].values), 1/len(self._trade_data))
        return all_share_index
