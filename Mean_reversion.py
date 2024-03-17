import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_k_reversal(df, window=13):
    # Calculate moving average
    df['MA'] = df['Close'].rolling(window=window).mean()
    
    # Calculate whether market is above its moving average
    df['Above_MA'] = (df['Close'] > df['MA']).astype(int)
    
    # Count consecutive occurrences of being above MA
    df['Consecutive_Above_MA'] = df['Above_MA'].diff().fillna(0)
    
    # Detect bullish and bearish signals
    df['Bullish_Signal'] = df['Consecutive_Above_MA'].apply(lambda x: 1 if x == -1 else 0)
    df['Bearish_Signal'] = df['Consecutive_Above_MA'].apply(lambda x: 1 if x >= 21 else 0)
    
    return df

def calculate_profit(initial_amount, ticker):
    # Download historical data using yfinance
    data = yf.download(ticker, start="2022-01-01", end="2024-01-01")

    # Calculate K's Reversal Indicator II signals
    data = calculate_k_reversal(data)

    # Initialize variables
    amount = initial_amount
    shares = 0
    entry_price = 0
    profit_percentage = 0
    buy_points = []
    sell_points = []

    # Iterate through each row in the data
    for index, row in data.iterrows():
        # Check if bullish signal and enough cash to buy
        if row['Bullish_Signal'] == 1 and amount > 0:
            # Calculate the number of shares to buy with available cash
            shares_to_buy = amount / row['Close']
            # Update the total number of shares
            shares += shares_to_buy
            # Update the amount of cash
            amount = 0
            # Set the entry price
            entry_price = row['Close']
            # Store buy point
            buy_points.append((index, row['Close']))
        # Check if bearish signal and have shares to sell
        elif row['Bearish_Signal'] == 1 and shares > 0:
            # Calculate the total sell amount
            sell_amount = shares * row['Close']
            # Calculate the profit
            profit = sell_amount - (shares * entry_price)
            # Update the total amount
            amount += sell_amount
            # Update the total profit percentage
            profit_percentage += (profit / initial_amount) * 100
            # Reset the number of shares
            shares = 0
            # Store sell point
            sell_points.append((index, row['Close']))

    return profit_percentage, buy_points, sell_points

def plot_signals(ticker, buy_points, sell_points):
    # Download historical data using yfinance
    data = yf.download(ticker, start="2022-01-01", end="2024-01-01")

    # Plot closing price
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Close Price', color='black')

    # Plot buy points
    for buy_point in buy_points:
        plt.scatter(buy_point[0], buy_point[1], color='green', marker='^', s=100, label='Buy')

    # Plot sell points
    for sell_point in sell_points:
        plt.scatter(sell_point[0], sell_point[1], color='red', marker='v', s=100, label='Sell')

    plt.title('Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage
ticker = "BTC-USD"  # Example ticker symbol
initial_amount = 10000
profit_percentage, buy_points, sell_points = calculate_profit(initial_amount, ticker)
print("Profit Percentage:", round(profit_percentage, 2), "%")

# Plot buy and sell signals
plot_signals(ticker, buy_points, sell_points)
