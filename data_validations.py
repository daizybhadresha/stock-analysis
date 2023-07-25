import logging

class DataValidations:

    @staticmethod
    def validate_non_zero(value, value_name):
        if int(value) <= 0:
            logging.error(f"The given {value_name} value {value} is invalid (cannot be less then or equal to 0)")

    @staticmethod
    def validate_indicator(value):
        if value.lower() not in ['sell','buy']:
            logging.error(f"Entered transaction type {value} is invalid, It can be either 'Buy' or 'Sell'") 
    
    @staticmethod
    def validate_symbol(value, symbol_list):
        if value.upper() not in symbol_list:
            logging.error(f"Entered Symbol {value} is invalid, It can be from one of these {symbol_list}") 
