import yfinance as yf
import talib
import pandas as pd
import matplotlib.pyplot as plt

# Function to generate buy signals
def generate_buy_signals(rsi, oversold_level, threshold_level):
    buy_signals = []
    for i in range(1, len(rsi)):
        if rsi.iloc[i - 1] <= oversold_level and rsi.iloc[i] > oversold_level and rsi.iloc[i] <= threshold_level:
            buy_signals.append(i)
    return buy_signals

# Function to generate sell signals
def generate_sell_signals(rsi, overbought_level, threshold_level):
    sell_signals = []
    for i in range(1, len(rsi)):
        if rsi.iloc[i - 1] >= overbought_level and rsi.iloc[i] < overbought_level and rsi.iloc[i] >= threshold_level:
            sell_signals.append(i)
    return sell_signals

# Function to calculate profit percentage
def calculate_profit(initial_amount, buy_price, sell_price):
    return ((sell_price - buy_price) / buy_price) * initial_amount

# Function to plot buy and sell points
def plot_signals(data, buy_signals, sell_signals):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Close Price', color='black')
    plt.scatter(data.iloc[buy_signals].index, data['Close'].iloc[buy_signals], marker='^', color='g', label='Buy Signal')
    plt.scatter(data.iloc[sell_signals].index, data['Close'].iloc[sell_signals], marker='v', color='r', label='Sell Signal')
    plt.title('Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Fetch stock data (replace 'AAPL' with your desired stock symbol)
    data = yf.download('TSLA', start='2021-11-01', end='2022-12-01')

    # Calculate RSI
    data['RSI'] = talib.RSI(data['Close'], timeperiod=5)

    # Parameters
    oversold_level = 20
    overbought_level = 80
    threshold_level = 33
    initial_amount = 10000

    # Generate signals
    buy_signals = generate_buy_signals(data['RSI'], oversold_level, threshold_level)
    sell_signals = generate_sell_signals(data['RSI'], overbought_level, threshold_level)


    # Calculate profit
    total_profit = 0
    for buy_index in buy_signals:
        for sell_index in sell_signals:
            if sell_index > buy_index:
                buy_price = data['Close'].iloc[buy_index]
                sell_price = data['Close'].iloc[sell_index]
                total_profit += calculate_profit(initial_amount, buy_price, sell_price)
                break

    # Calculate profit percentage
    profit_percentage = (total_profit / initial_amount) * 100

    # Print profit percentage
    print("Total profit in percentage:", profit_percentage)

    # Plot buy and sell signals
    plot_signals(data, buy_signals, sell_signals)


