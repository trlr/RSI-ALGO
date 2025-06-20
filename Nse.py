import yfinance as yf
import pandas as pd
import ta
import matplotlib.pyplot as plt

# Parameters
symbol = 'RELIANCE.NS'
interval = '1D'  # Options: '1m', '5m', '15m', '1h', '1d'
period = '6mo'   # Last 6 months

# Step 1: Download historical data
df = yf.download(symbol, interval=interval, period=period)

# Step 2: Calculate RSI
rsi_indicator = ta.momentum.RSIIndicator(close=df['Close'].squeeze(), window=14)

df['RSI'] = rsi_indicator.rsi()

# Step 3: Create Buy/Sell signal columns
df['Signal'] = None
df.loc[df['RSI'] < 30, 'Signal'] = 'Buy'
df.loc[df['RSI'] > 70, 'Signal'] = 'Sell'

# Step 4: Filter Buy/Sell rows
buy_signals = df[df['Signal'] == 'Buy']
sell_signals = df[df['Signal'] == 'Sell']

# Step 5: Print signals
print("Buy Signals:")
print(buy_signals[['Close', 'RSI']])

print("\nSell Signals:")
print(sell_signals[['Close', 'RSI']])

# Optional Step 6: Plotting
plt.figure(figsize=(14, 7))

# Price
plt.plot(df.index, df['Close'], label='Close Price', color='blue', alpha=0.5)

# Mark Buy/Sell
plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal (RSI < 30)', s=100)
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal (RSI > 70)', s=100)

plt.title(f'{symbol} - Buy/Sell based on RSI')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
