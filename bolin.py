import yfinance as yf
import numpy as np
from talib import RSI

# Function to generate bullish signal
def generate_bullish_signal(current_low, previous_open, previous_rsi_8, previous_rsi_12):
    if current_low < previous_open and previous_rsi_8 < 50 and previous_rsi_8 > 35:
        if all(rsi < 35 for rsi in previous_rsi_12):
            return True
    return False

# Function to generate bearish signal
def generate_bearish_signal(current_high, previous_open, previous_rsi_8, previous_rsi_12):
    if current_high > previous_open and previous_rsi_8 > 50 and previous_rsi_8 < 65:
        if all(rsi > 65 for rsi in previous_rsi_12):
            return True
    return False

# Function to calculate profit percentage
def calculate_profit_percentage(initial_price, final_price):
    return ((final_price - initial_price) / initial_price) * 100

# Function to apply the strategy and calculate profit
def backtest_strategy(ticker_symbol, initial_amount):
    # Download historical data
    data = yf.download(ticker_symbol, start="2022-01-01", end="2024-01-01")
    
    # Calculate RSI
    data['RSI_8'] = RSI(data['Close'], timeperiod=8)
    data['RSI_12'] = RSI(data['Close'], timeperiod=12)
    
    # Initialize variables
    total_trades = 0
    total_profit = 0
    current_balance = initial_amount
    
    for i in range(1, len(data)):
        current_low = data['Low'].iloc[i]
        current_high = data['High'].iloc[i]
        previous_open = data['Open'].iloc[i-1]
        previous_rsi_8 = data['RSI_8'].iloc[i-1]
        previous_rsi_12 = data['RSI_12'].iloc[i-1:i-13:-1].tolist()
        
        if generate_bullish_signal(current_low, previous_open, previous_rsi_8, previous_rsi_12):
            buy_price = data['Close'].iloc[i]
            max_buy_amount = current_balance * 0.25
            buy_amount = min(max_buy_amount, current_balance)
            buy_quantity = buy_amount / buy_price
            current_balance -= buy_amount
            total_trades += 1
        elif generate_bearish_signal(current_high, previous_open, previous_rsi_8, previous_rsi_12):
            if total_trades > 0:
                sell_price = data['Close'].iloc[i]
                total_profit += calculate_profit_percentage(buy_price, sell_price) * buy_quantity
                current_balance += buy_quantity * sell_price
                total_trades -= 1
    
    average_profit = total_profit / initial_amount * 100 if initial_amount > 0 else 0
    return average_profit

# Example usage:
ticker_symbol = "TSLA"
initial_amount = 10000
profit_percentage = backtest_strategy(ticker_symbol, initial_amount)
print("Profit percentage:", profit_percentage)
