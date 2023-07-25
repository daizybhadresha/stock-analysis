import pandas as pd
import numpy as np
import datetime
from data_validations import DataValidations
import logging

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
        self._trade_data = pd.DataFrame()
        data = [['TEA','Common',0,np.nan,100],['POP','Common',8,np.nan,100],['ALE','Common',23,np.nan,60],
                ['GIN','Preferred',8,2,100],['JOE','Common',13,np.nan,250]]
        self._stock_data = pd.DataFrame(data,
                                columns = [self.STOCK_SYMBOL_COL,self.S_STOCK_TYPE_COL,self.S_LAST_DIVIDEND_COL,self.S_FIXED_DIVIDEND_COL,self.S_PAR_VALUE_COL]
                            )

    def record_trade(self, timestamp: str, stock_symbol: str, trans_type: str, volume: float, price: float):
        '''
            Adds new trade entry to the dataframe
            Args:
                timestamp : str : Exact date time of the trade
                stock_symbol : str : Stock symbol (shortform of the stock)
                trans_type : str : Buy or Sell operation
                volume: float : Quantity of the stocks
                price: float : Price of the stock
            Returns:
                None
        '''
        if timestamp == None:
            timestamp = datetime.datetime.now().strftime(("%m-%d-%Y %H:%M:%S"))
        
        entry = { self.T_TIMESTAMP_COL: timestamp, 
                    self.STOCK_SYMBOL_COL: DataValidations.validate_symbol(stock_symbol, self._stock_data[self.STOCK_SYMBOL_COL].tolist()),
                    self.T_QUANTITY_COL: DataValidations.validate_non_zero(volume,"Stock quantity"),
                    self.T_INDICATOR_COL: DataValidations.validate_indicator(trans_type),
                    self.T_TRADED_PRICE_COL: DataValidations.validate_non_zero(price,"Stock price")}
        
        self._trade_data = self._trade_data.append(entry,ignore_index=True)
        logging.info("A new transaction record added")

    def get_recorded_trade(self):
        '''
            Returns current trade data
            Returns:
                Trade details dataframe
        '''
        if len(self._trade_data) > 0:
            return self._trade_data
        else:
            logging.info("Trading data is empty")
        return None

    def load_stock_info(self, stock_symbol: str):
        '''
            Returns stock related information based on stock symbol in parameter
            Args:
                stock_symbol : str : Stock symbol (shortform of the stock)
            Returns:
                stock_type : str : Common/Preferred
                last_dividend : float : Last dividend calculated
                fixed_dividend : float : Fixed dividend calculated
                par_value : float : Par value of share
        '''
        DataValidations.validate_symbol(stock_symbol, self._stock_data[self.STOCK_SYMBOL_COL].tolist())
        required_stock = self._stock_data[self._stock_data[self.STOCK_SYMBOL_COL] == stock_symbol]
        stock_type = required_stock[self.S_STOCK_TYPE_COL].item()
        last_dividend = required_stock[self.S_LAST_DIVIDEND_COL].item()
        fixed_dividend = required_stock[self.S_FIXED_DIVIDEND_COL].item()
        par_value = required_stock[self.S_PAR_VALUE_COL].item()
        return stock_type, last_dividend, fixed_dividend, par_value

    def calculate_dividend(self, stock_symbol: float, stock_price: float):
        '''
            Calculates dividend based on the stock type (Common/Preferred)
            Args:
                stock_symbol : str : Stock symbol (shortform of the stock)
                stock_price: float : Price of the stock
            Returns:
                dividend : float : Calculated dividend
        '''
        DataValidations.validate_non_zero(stock_price,"Stock price")
        DataValidations.validate_symbol(stock_symbol, self._stock_data[self.STOCK_SYMBOL_COL].tolist())
        stock_type, last_dividend, fixed_dividend, par_value = self.load_stock_info(stock_symbol)
        dividend = None
        if stock_type == self.TYPE_COMMON:
            dividend = last_dividend/stock_price
        elif stock_type == self.TYPE_PREFERRED:
            dividend = (fixed_dividend * par_value)/stock_price
        else:
            logging.info("Unable to calculate dividend, Encountered unknown stock type")
        return dividend

    def calculate_pe_ratio(self, stock_symbol: str, stock_price: float):
        '''
            Calculates price to earnings ratio for a stock symbol
            Args:
                stock_symbol : str : Stock symbol (shortform of the stock)
                stock_price: float : Price of the stock
            Returns:
                pe_ratio : float : Calculated PE ratio
        '''
        DataValidations.validate_non_zero(stock_price,"Stock price")
        DataValidations.validate_symbol(stock_symbol, self._stock_data[self.STOCK_SYMBOL_COL].tolist())
        dividend = self.calculate_dividend(stock_symbol, stock_price)
        pe_ratio = None
        if dividend > 0:
            pe_ratio = stock_price/dividend
        else:
            logging.info("Calculated dividend for stock is ", dividend,", Price to Earnings ratio cannot be calculated")
        return pe_ratio

    def volume_weighted_stock_price(self, stock_symbol: str):
        '''
            Calculates volume weighted stock for the past 15 minutes
            Args:
                stock_symbol : str : Stock symbol (shortform of the stock)
            Returns:
                vwsp : float : Calculated volume weighted stock
        '''
        DataValidations.validate_symbol(stock_symbol, self._stock_data[self.STOCK_SYMBOL_COL].tolist())
        timestamp_fifteen_mins_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
        price_multiply_quantity = 0
        total_quantity = 0
        for row in self._trade_data:
            if row[self.T_TIMESTAMP_COL] >= timestamp_fifteen_mins_ago and row[self.STOCK_SYMBOL_COL]==stock_symbol:
                price_multiply_quantity = price_multiply_quantity + (row[self.T_QUANTITY_COL] * row[self.T_TRADED_PRICE_COL])
                total_quantity = total_quantity + row[self.T_QUANTITY_COL]
        
        total_quantity = 1 if total_quantity == 0 else total_quantity
        vwsp = price_multiply_quantity / total_quantity
        return vwsp

    def calculate_all_share_index(self):
        '''
            Calculates all share index of all stocks
            Returns:
                all_share_index : float
        '''
        all_share_index = None
        if len(self._trade_data) > 0:
            all_share_index = np.power(np.prod(self._trade_data[self.T_TRADED_PRICE_COL].values), 1/len(self._trade_data))
        else:
            logging.info("No trade data for calculations")
        return all_share_index
