import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

symbol = "AAPL"
data = yf.download(symbol, period="60d", interval="1d")

window = 20
std_multiplier = 2

# Hitung Bollinger Bands manual
data['rolling_mean'] = data['Close'].rolling(window=window).mean()
data['rolling_std'] = data['Close'].rolling(window=window).std()
data['bb_upper'] = data['rolling_mean'] + (std_multiplier * data['rolling_std'])
data['bb_lower'] = data['rolling_mean'] - (std_multiplier * data['rolling_std'])

# Plot hasilnya
plt.figure(figsize=(12,6))
plt.plot(data.index, data['Close'], label='Close')
plt.plot(data.index, data['bb_upper'], label='Upper Band')
plt.plot(data.index, data['rolling_mean'], label='Middle Band')
plt.plot(data.index, data['bb_lower'], label='Lower Band')
plt.legend()
plt.title(f"Bollinger Bands for {symbol}")
plt.show()
